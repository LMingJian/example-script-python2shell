import yaml

stream = open('026Yaml示例文件.yaml', mode='r', encoding='utf-8')
d = yaml.load(stream, Loader=yaml.FullLoader)
print(d)
stream.close()
