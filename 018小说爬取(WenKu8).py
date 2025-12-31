import re
from os import path, mkdir
from time import sleep

import requests
from bs4 import BeautifulSoup

"""
A: 对网站WenKu8的爬虫，使用requests，BeautifulSoup实现对接口的爬取
   由于该网站关闭了对外搜索功能，未登录下不允许进行搜索，于是使用Bing代替搜索功能
   网站书本的书本ID，由搜索功能获取，如搜索结果链接：https://www.wenku8.net/novel/1/1143/index.htm，则书本ID为1143
   使用书本ID拼接txt下载文本链接，由浏览器下载txt文本
   使用书本ID，执行插图下载功能，由request下载插图
PS: 插图接口：http://dl.wenku8.com/pack.php?aid=bookID&vid=chapterID
    txt下载接口：http://dl.wenku8.com/down.php?type=txt&id=bookID&fname=bookName  好像要验权了
    txt另一个下载接口：http://dl.wenku8.com/txtgbk/index/bookID.txt  index和ID需要提供，参照书本详情页链接内容
"""


class WenKu8:
    _searchUrl = "https://cn.bing.com"
    _searchApi = "/search"
    _baseUrl = "https://www.wenku8.net/book/"
    _dlUrl = "http://dl.wenku8.com"
    _packApi = "/pack.php"
    _textApi = '/down.php'
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70",
    }
    _road = "D:\\ZResult\\"
    _dirName = ''
    _picture = []

    def search(self):
        print("====================")
        print("1.搜索")
        print("====================")
        string = input('请输入关键字: ')
        params = {'q': string+' wenku8.net'}
        try:
            response = requests.request('GET', self._searchUrl + self._searchApi, headers=self._headers, params=params)
        except BaseException as e:
            print('请求失败')
            print(e)
            return 0
        li = BeautifulSoup(response.text, 'html.parser').find_all('li', class_='b_algo')
        print("====================")
        for each in li:
            h2 = each.find('h2')
            href = h2.a.get('href')
            if 'wenku8.net' not in href:
                continue
            print(href)
            print(h2.a.text)
            print("====================")

    def dl_pack(self):
        print("====================")
        print("2.下载插图")
        print("====================")
        aid = input('请输入ID: ')
        if aid == 'exit':
            return 0
        response = requests.request('GET', self._baseUrl + aid + '.htm', headers=self._headers)
        content_url = BeautifulSoup(response.text, 'html.parser').find_all('fieldset')[0].div.a.get('href')
        response = requests.request('GET', content_url, headers=self._headers)
        td = BeautifulSoup(response.text.encode('ISO-8859-1').decode('GBK'), 'html.parser').find_all('td')
        link = []
        name = []
        for each in td:
            if each.get('class') == ['vcss']:
                link.append(each.text)
                name.append(each.text)
            elif each.get('class') == ['ccss']:
                # noinspection PyBroadException
                try:
                    link.append(each.a.get('href'))
                    name.append(each.a.text)
                except BaseException:
                    continue
        print('目录获取成功')
        for each in link:
            sleep(5)
            if '.htm' not in each:
                if self._picture and self._dirName:
                    print('总数: '+str(len(self._picture)))
                    for p in self._picture:
                        time = 0
                        while time <= 4:
                            time += 1
                            # noinspection PyBroadException
                            try:
                                paths = self._road + self._dirName + '\\' + str(self._picture.index(p)) + 'pic.jpg'
                                if path.exists(paths):
                                    break
                                response = requests.request("GET", p, headers=self._headers)
                                sleep(1)
                                with open(paths, 'wb') as pic:
                                    pic.write(response.content)
                                break
                            except BaseException:
                                sleep(2)
                                if time == 5:
                                    print('error: '+p)
                                continue
                    self._picture.clear()
                print(each)
                self._dirName = name[link.index(each)]
                if not path.exists(self._road + self._dirName):
                    mkdir(self._road + self._dirName)
                continue
            else:
                paths = self._road + self._dirName + '\\' + name[link.index(each)] + '.txt'
                paths = re.sub('[<>/]', '', paths)
                if not path.exists(paths):
                    with open(paths, 'wb') as f:
                        f.write('空'.encode('UTF-8'))
                params = {
                    'aid': aid,
                    'vid': each.replace('.htm', ''),
                }
                response = requests.request('GET', self._dlUrl + self._packApi, headers=self._headers, params=params)
                div = BeautifulSoup(response.text.encode('ISO-8859-1').decode('UTF-8', 'ignore'), 'html.parser')
                div = div.find_all('div', class_='divimage')
                for node in div:
                    if node.get('title') not in self._picture:
                        self._picture.append(node.get('title'))
        print("====================")
        print('请到 D:/ZResult 查看结果')
        print("====================")

    def dl_text(self):
        print("====================")
        print("3.下载txt文本(不包括插图)")
        print("====================")
        aid = input('请输入ID: ')
        if aid == 'exit':
            return 0
        print('请点击以下链接使用浏览器下载')
        print(self._dlUrl+self._textApi+'?type={}&id={}&fname={}'.format('txt', aid, aid))
        print("====================")

    def menu(self):
        print("====================")
        print("欢迎进入系统")
        print("====================")
        print('1.搜索')
        print('2.下载txt文本(不包括插图)')
        print('3.下载插图')
        print('6.退出')
        print("====================")
        while True:
            flag = input('请选择功能: ')
            if flag == '1':
                self.search()
            elif flag == '2':
                self.dl_text()
            elif flag == '3':
                self.dl_pack()
            elif flag == '6':
                break
            else:
                print('无此功能')
                continue
        print('退出系统')


if __name__ == '__main__':
    WenKu8().menu()
