import os
import time
import urllib.request
"""
Q: 如何通过链接进行下载
"""


def download_with_file():
    """
    A: 将链接一行一行写入文件，读取可以实现批量下载
    """
    now = time.strftime("%Y.%m.%d[%H%M%S]")
    with open('链接文件.txt', 'r', encoding='UTF-8') as f:
        url = f.readlines()
        for each in url:
            link = each.replace('\n', '').replace('\r', '')
            filename = os.path.join(now+'.jpg')
            print("正在下载", filename)
            urllib.request.urlretrieve(link, filename)
            print("成功下载！")


def download_with_url(url):
    try:
        now = time.strftime("%Y.%m.%d[%H%M%S]")
        filename = os.path.join(now+'.jpg')
        print("正在下载", filename)
        urllib.request.urlretrieve(url, filename)
        print("成功下载！")
    except BaseException as e:
        print("下载失败！")
        print(e)


if __name__ == '__main__':
    urls = 'https://uploadfile.bizhizu.cn/2014/0710/20140710105210540.jpg'
    download_with_url(urls)
