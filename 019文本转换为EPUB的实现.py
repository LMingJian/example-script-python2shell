import os
"""
A: 实现将txt文本文件转换为epub文件专用的xhtml
   最终成书需要配合Sigil使用
   脚本将寻找路径rootRoad里所有的txt文件，对每个文件进行读取，将结果写入列表result，并添加xhtml头尾
   最后将result按行写入resultRoad文件夹内，以xhtml保存
"""
rootRoad = r"F:\PythonProject"
resultRoad = r'F:\PythonProject'


def write(result, chap):
    if not os.path.exists(resultRoad):
        os.mkdir(resultRoad)
    road = os.path.join(resultRoad, chap.replace('.txt', '.xhtml'))
    with open(road, 'wb') as file:
        for each in result:
            file.write(each.encode('UTF-8'))
            file.write('\n'.encode('UTF-8'))

        
def epub_build():
    print('书籍制作中')
    dirs = os.listdir(rootRoad)
    for each in dirs:
        if '.txt' not in each:
            continue
        file = open(os.path.join(rootRoad, each), 'r', encoding='UTF-8')
        book = file.readlines()
        result = ['<?xml version="1.0" encoding="utf-8"?>',
                  '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">',
                  '<html xmlns="http://www.w3.org/1999/xhtml">',
                  f'<head>\n\t<title>{each.replace(".txt", "")}</title>\n</head>\n<body>\n',
                  ]
        # 添加正文
        for content in book:
            if book.index(content) == 0:
                content = content.replace('\n', '').replace('\r', '')
                result.append(f"<h3>{content}</h3>\n")
                continue
            content = content.replace('\n', '').replace('\r', '')
            if content != '':
                result.append(f'<p>{content}</p>')
        # 添加尾
        result.append('\n</body>\n</html>')
        write(result, each)
        file.close()
    print('书籍制作完成')


if __name__ == "__main__":
    epub_build()
