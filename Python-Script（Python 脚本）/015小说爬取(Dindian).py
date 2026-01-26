import bs4.element
import requests
from bs4 import BeautifulSoup
"""
A: 使用requests, BeautifulSoup实现的小说爬取，通过接口实现对内容的爬取。
   优点快速，但不稳定，当网站对接口权限验证严重时会出现问题
"""


class DinDian:
    _baseUrl = "https://www.dingdiann.net"
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70",
    }
    _chapter = []
    _link = []

    def search(self):
        print("====================")
        print("1.搜索")
        print("====================")
        string = input('请输入关键字: ')
        api = '/searchbook.php'
        page = 1
        while True:
            params = {
                'keyword': string,
                'page': str(page),
            }
            try:
                response = requests.request('GET', self._baseUrl + api, headers=self._headers, params=params)
            except BaseException as e:
                print('请求失败')
                print(e)
                return 0
            soup = BeautifulSoup(response.text, 'html.parser')
            div = soup.find('div', class_='novelslist2')
            soup = BeautifulSoup(str(div), 'html.parser')
            a = soup.find_all('a')
            if_name = True
            print('====================')
            print("name | url")
            for each in a:
                if if_name:
                    print(each.string, end=' | ')
                    print(each.get('href'))
                    if_name = not if_name
                else:
                    if_name = not if_name
            print('====================')
            flag = input('下一页(N/n),上一页(B/b),结束(其他): ')
            if flag in ['n', 'N']:
                page = page + 1
            elif flag in ['b', 'B']:
                page = page - 1
            else:
                break
        print('结束搜索')
        print('====================')

    def get_chapter(self, string):
        try:
            response = requests.request('GET', self._baseUrl + string, headers=self._headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            div = soup.find('dl')
            soup = BeautifulSoup(str(div), 'html.parser')
            a = soup.find_all('a')
            for each in a:
                if each.get('href') not in self._link:
                    self._link.append(each.get('href'))
                    self._chapter.append(each.string)
                else:
                    self._link.remove(each.get('href'))
                    self._chapter.remove(each.string)
                    self._link.append(each.get('href'))
                    self._chapter.append(each.string)
            return 1
        except BaseException as e:
            return e

    def read(self):
        print("====================")
        print("2.阅读")
        print("====================")
        string = input('请输入链接: ')
        if self.get_chapter(string) == 1:
            print('获取章节成功')
            current = 0
            chap = input('请选择章节(q退出): ')
            if chap == 'q':
                return 0
            try:
                chap = int(chap)
            except BaseException as e:
                print(e)
                print('跳转失败')
                chap = 1
            for each in self._link:
                current += 1
                if current < chap:
                    continue
                try:
                    response = requests.request('GET', self._baseUrl + each, headers=self._headers)
                except BaseException as e:
                    print('请求失败')
                    print(e)
                    self._link.clear()
                    self._chapter.clear()
                    return 0
                soup = BeautifulSoup(response.text, 'html.parser')
                div = soup.find('div', id='content')
                print("------------------------")
                print(self._chapter[self._link.index(each)])
                print("------------------------")
                count = 0
                for node in div:
                    if isinstance(node, bs4.element.NavigableString):
                        print(node.strip())
                        count += 1
                    if count == 5:
                        print("------------------------")
                        if input('继续打印(q退出): ') == 'q':
                            break
                        else:
                            count = 0
                        print("------------------------")
                if input('下一章(q退出): ') == 'q':
                    break
            self._link.clear()
            self._chapter.clear()
        else:
            print('系统错误')
            self._link.clear()
            self._chapter.clear()

    def menu(self):
        print("====================")
        print("欢迎进入系统")
        print("====================")
        print('1.搜索')
        print('2.阅读')
        print('6.退出')
        print("====================")
        while True:
            flag = input('请选择功能: ')
            if flag == '1':
                self.search()
            elif flag == '2':
                self.read()
            elif flag == '6':
                break
            else:
                print('无此功能')
                continue
        print('退出系统')


if __name__ == "__main__":
    DinDian().menu()
