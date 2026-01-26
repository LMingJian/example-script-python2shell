import os
import sys
import gzip
import json
import hashlib
import shutil
import requests
import tarfile
import urllib3

urllib3.disable_warnings()

if len(sys.argv) != 2:
    print('Usage:\n\tdocker-pull.py [registry/][repository/]image[:tag|@digest]\n')
    exit(1)

# Look for the Docker image to download
repo = 'library'
tag = 'latest'
img_parts = sys.argv[1].split('/')
try:
    img, tag = img_parts[-1].split('@')
except ValueError:
    try:
        img, tag = img_parts[-1].split(':')
    except ValueError:
        img = img_parts[-1]
# Docker client doesn't seem to consider the first element as a potential registry unless there is a '.' or ':'
if len(img_parts) > 1 and ('.' in img_parts[0] or ':' in img_parts[0]):
    registry = img_parts[0]
    repo = '/'.join(img_parts[1:-1])
else:
    registry = 'registry-1.docker.io'
    if len(img_parts[:-1]) != 0:
        repo = '/'.join(img_parts[:-1])
    else:
        repo = 'library'
repository = '{}/{}'.format(repo, img)

# Get Docker authentication endpoint when it is required
auth_url = 'https://auth.docker.io/token'
reg_service = 'registry.docker.io'
resp = requests.get('https://{}/v2/'.format(registry), verify=False)
if resp.status_code == 401:
    auth_url = resp.headers['WWW-Authenticate'].split('"')[1]
    try:
        reg_service = resp.headers['WWW-Authenticate'].split('"')[3]
    except IndexError:
        reg_service = ""

# Get Docker token (this function is useless for unauthenticated registries like Microsoft)
def get_auth_head(accept_type):
    response = requests.get('{}?service={}&scope=repository:{}:pull'.format(auth_url, reg_service, repository),
                        verify=False)
    access_token = response.json()['token']
    auth_header = {'Authorization': 'Bearer ' + access_token, 'Accept': accept_type}
    return auth_header

# Docker style progress bar
def progress_bar(blob, traits):
    sys.stdout.write('\r' + blob[7:19] + ': Downloading [')
    for i in range(0, traits):
        if i == traits - 1:
            sys.stdout.write('>')
        else:
            sys.stdout.write('=')
    for i in range(0, 49 - traits):
        sys.stdout.write(' ')
    sys.stdout.write(']')
    sys.stdout.flush()

# Fetch manifest v2 and get image layer digests
auth_head = get_auth_head('application/vnd.docker.distribution.manifest.v2+json')
resp = requests.get('https://{}/v2/{}/manifests/{}'.format(registry, repository, tag), headers=auth_head, verify=False)
if resp.status_code != 200:
    print('[-] Cannot fetch manifest for {} [HTTP {}]'.format(repository, resp.status_code))
    print(resp.content)
    auth_head = get_auth_head('application/vnd.docker.distribution.manifest.list.v2+json')
    resp = requests.get('https://{}/v2/{}/manifests/{}'.format(registry, repository, tag), headers=auth_head,
                        verify=False)
    if resp.status_code == 200:
        print('[+] Manifests found for this tag (use the @digest format to pull the corresponding image):')
        manifests = resp.json()['manifests']
        for manifest in manifests:
            for key, value in manifest["platform"].items():
                sys.stdout.write('{}: {}, '.format(key, value))
            print('digest: {}'.format(manifest["digest"]))
    exit(1)
layers = resp.json()['layers']

# Create tmp folder that will hold the image
imgdir = 'tmp_{}_{}'.format(img, tag.replace(':', '@'))
os.mkdir(imgdir)
print('Creating image structure in: ' + imgdir)

config = resp.json()['config']['digest']
conf_resp = requests.get('https://{}/v2/{}/blobs/{}'.format(registry, repository, config), headers=auth_head,
                        verify=False)
file = open('{}/{}.json'.format(imgdir, config[7:]), 'wb')
file.write(conf_resp.content)
file.close()

content = [{
    'Config': config[7:] + '.json',
    'RepoTags': [],
    'Layers': []
}]
if len(img_parts[:-1]) != 0:
    content[0]['RepoTags'].append('/'.join(img_parts[:-1]) + '/' + img + ':' + tag)
else:
    content[0]['RepoTags'].append(img + ':' + tag)

empty_json = '{"created":"1970-01-01T00:00:00Z","container_config":{"Hostname":"","Domainname":"","User":"","AttachStdin":false, \
	"AttachStdout":false,"AttachStderr":false,"Tty":false,"OpenStdin":false, "StdinOnce":false,"Env":null,"Cmd":null,"Image":"", \
	"Volumes":null,"WorkingDir":"","Entrypoint":null,"OnBuild":null,"Labels":null}}'

# Build layer folders
parent_id = ''
fake_layer_id = ''
for layer in layers:
    u_blob = layer['digest']
    # FIX-ME: Creating fake layer ID. Don't know how Docker generates it
    fake_layer_id = hashlib.sha256((parent_id + '\n' + u_blob + '\n').encode('utf-8')).hexdigest()
    layer_dir = imgdir + '/' + fake_layer_id
    os.mkdir(layer_dir)

    # Creating VERSION file
    file = open(layer_dir + '/VERSION', 'w')
    file.write('1.0')
    file.close()

    # Creating layer.tar file
    sys.stdout.write(u_blob[7:19] + ': Downloading...')
    sys.stdout.flush()
    auth_head = get_auth_head(
        'application/vnd.docker.distribution.manifest.v2+json')  # refreshing token to avoid its expiration
    b_resp = requests.get('https://{}/v2/{}/blobs/{}'.format(registry, repository, u_blob), headers=auth_head,
                         stream=True, verify=False)
    if b_resp.status_code != 200:  # When the layer is located at a custom URL
        b_resp = requests.get(layer['urls'][0], headers=auth_head, stream=True, verify=False)
        if b_resp.status_code != 200:
            print('\rERROR: Cannot download layer {} [HTTP {}]'.format(u_blob[7:19], b_resp.status_code,
                                                                       b_resp.headers['Content-Length']))
            print(b_resp.content)
            exit(1)
    # Stream download and follow the progress
    b_resp.raise_for_status()
    unit = int(b_resp.headers['Content-Length']) / 50
    acc = 0
    nb_traits = 0
    progress_bar(u_blob, nb_traits)
    with open(layer_dir + '/layer_gzip.tar', "wb") as file:
        for chunk in b_resp.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                acc = acc + 8192
                if acc > unit:
                    nb_traits = nb_traits + 1
                    progress_bar(u_blob, nb_traits)
                    acc = 0
    sys.stdout.write("\r{}: Extracting...{}".format(u_blob[7:19], " " * 50))  # Ugly but works everywhere
    sys.stdout.flush()
    with open(layer_dir + '/layer.tar', "wb") as file:  # Decompress gzip response
        unzLayer = gzip.open(layer_dir + '/layer_gzip.tar', 'rb')
        shutil.copyfileobj(unzLayer, file)  # noqa
        unzLayer.close()
    os.remove(layer_dir + '/layer_gzip.tar')
    print("\r{}: Pull complete [{}]".format(u_blob[7:19], b_resp.headers['Content-Length']))
    content[0]['Layers'].append(fake_layer_id + '/layer.tar')

    # Creating JSON file
    file = open(layer_dir + '/json', 'w')
    # last layer = config manifest - history - rootfs
    if layers[-1]['digest'] == layer['digest']:
        # FIX-ME: json.loads() automatically converts to Unicode, thus decoding values whereas Docker doesn't
        json_obj = json.loads(conf_resp.content)
        del json_obj['history']
        try:
            del json_obj['rootfs']
        except:  # noqa, Because Microsoft loves case insensitiveness
            del json_obj['rootfS']
    else:  # other layers JSON are empty
        json_obj = json.loads(empty_json)
    json_obj['id'] = fake_layer_id
    if parent_id:
        json_obj['parent'] = parent_id
    parent_id = json_obj['id']
    file.write(json.dumps(json_obj))
    file.close()

file = open(imgdir + '/manifest.json', 'w')
file.write(json.dumps(content))
file.close()

if len(img_parts[:-1]) != 0:
    content = {'/'.join(img_parts[:-1]) + '/' + img: {tag: fake_layer_id}}
else:  # when pulling only an img (without repo and registry)
    content = {img: {tag: fake_layer_id}}
file = open(imgdir + '/repositories', 'w')
file.write(json.dumps(content))
file.close()

# Create image tar and clean tmp folder
docker_tar = repo.replace('/', '_') + '_' + img + '.tar'
sys.stdout.write("Creating archive...")
sys.stdout.flush()
tar = tarfile.open(docker_tar, "w")
tar.add(imgdir, arcname=os.path.sep)
tar.close()
shutil.rmtree(imgdir)
print('\rDocker image pulled: ' + docker_tar)
