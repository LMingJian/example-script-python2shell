import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

ip = ''
file_name = ''
file_path = ''
boundary = ''
bearer_token = ''


def upload_file():
    api = f'http://{ip}/upload'
    data = MultipartEncoder(fields={
        'file_name': file_name,
        'format': 'jpg',
        'resource_file': (file_name, open(file_path, 'rb'), 'image/jpeg')
    }, boundary=boundary)
    headers = {'Authorization': bearer_token,
               'Content-Type': data.content_type}
    response = requests.request('POST', url=api, data=data, headers=headers)
    print(response.json())


if __name__ == '__main__':
    upload_file()

"""
文件上传，使用 MultipartEncoder 时会将参数转换为 WebKitFormBoundarykt 格式的内容传递
转换后格式示例如下

------WebKitFormBoundarykt2IbmHxt8Wg0teX
Content-Disposition: form-data; name="file_name"

科技.jpg
------WebKitFormBoundarykt2IbmHxt8Wg0teX
Content-Disposition: form-data; name="folder_id"

41
------WebKitFormBoundarykt2IbmHxt8Wg0teX
Content-Disposition: form-data; name="type"

3
------WebKitFormBoundarykt2IbmHxt8Wg0teX
Content-Disposition: form-data; name="format"

jpg
------WebKitFormBoundarykt2IbmHxt8Wg0teX
Content-Disposition: form-data; name="resource_file"; filename="科技.jpg"
Content-Type: image/jpeg

二进制数据
------WebKitFormBoundarykt2IbmHxt8Wg0teX--
"""