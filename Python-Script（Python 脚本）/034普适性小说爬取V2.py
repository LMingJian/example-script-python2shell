import os
import re
import threading
from time import sleep
from typing import Union

import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Edge, EdgeOptions, Keys
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

"""
1.V2版本将书源数据添加于脚本中，不再以文件存在
2.新增多线程下载功能
3.书源要求：
  a.存在搜索栏且支持Enter搜索
  b.搜索结果展示不打开新标签
  c.从目录页打开文章不会打开新标签
"""


class SeleniumSourceData:

    source_model = 'Selenium'

    def __init__(self, url, css_search, css_search_link, css_chap_link,
                 css_content_name, css_content, css_next,
                 message=None):
        self.url = url
        self.css_search = css_search
        self.css_search_link = css_search_link
        self.css_chap_link = css_chap_link
        self.css_content_name = css_content_name
        self.css_content = css_content
        self.css_next = css_next
        self.message = message


class ApiSourceData:

    source_model = 'Api'

    def __init__(self, url, search_method, search_url, search_key,
                 search_rule, catalo_rule, conten_rule, conten_next,
                 message=None, headers=None):
        self.url = url
        self.search_method = search_method
        self.search_url = search_url
        self.search_key = search_key
        self.search_rule = search_rule
        self.catalo_rule = catalo_rule
        self.conten_rule = conten_rule
        self.conten_next = conten_next
        self.message = message
        self.headers = headers


class SeleniumSource:

    # 需使用 Firefox 否则部分界面无法加载
    siluke_data = SeleniumSourceData(
        'https://www.siluke.com', '#searchkey', '.s2 a', '#list a',
        '#title h1', '#content', '#details a:nth-child(3)'
    )


class ApiSource:

    yiqi_data = ApiSourceData(
        'https://www.1qxs.com', 'GET', 'https://www.1qxs.com/search.html', 'kw',
        '.book .name a', '.catalog .list a', '.content', conten_next='.next a',
        message='replace: /xs -> /list', headers={'Cookie': 'uid=a0b5e379a1dc47e58f8d683f0330625f'}
    )


class Book:

    _model = 'Selenium'
    _edge_options = EdgeOptions()
    _firefox_options = FirefoxOptions()
    _edge_options.add_argument("headless")
    _firefox_options.add_argument("-headless")
    _firefox_driver_path = r'F:\PythonProject\WebDrive\geckodriver.exe'
    _edge_driver_path = r'F:\PythonProject\WebDrive\msedgedriver.exe'

    def __init__(self, source: Union[SeleniumSourceData, ApiSourceData]):
        """ browser: 1 -> Edge  other -> Firefox """
        self._model = source.source_model
        self._source = source
        if self._model == 'Selenium':
            # self._browser = Edge(service=Service(executable_path=self._edge_driver_path), options=self._edge_options)
            self._browser = Firefox(service=Service(executable_path=self._firefox_driver_path),
                                    options=self._firefox_options)
            self._browser.maximize_window()
            self._browser.implicitly_wait(6)
        elif self._model == 'Api':
            self._headers = {"User-Agent": "PostmanRuntime/7.29.2"}
            if self._source.headers is not None:
                self._headers.update(self._source.headers)

    def test(self):
        if self._model == 'Selenium':
            self._browser.get('https://www.baidu.com')
            print(self._browser.current_url)
        elif self._model == 'Api':
            response = requests.get('https://www.baidu.com', headers=self._headers)
            print(response.status_code)
        else:
            print('Disable Model')

    @staticmethod
    def _mirror(string):
        temp = list(string)
        temp.reverse()
        try:
            return "".join(each for each in temp)
        except KeyError:
            return "INVALID"

    def _search(self):
        print("====================")
        print("1.搜索")
        print("====================")
        key = input('请输入关键字(exit-退出): ')
        if key == 'exit':
            return 0
        chap_text = []
        chap_link = []
        if self._model == 'Selenium':
            self._browser.get(self._source.url)
            element = self._browser.find_element(By.CSS_SELECTOR, self._source.css_search)
            element.clear()
            element.send_keys(key)
            element.send_keys(Keys.ENTER)
            link = self._browser.find_elements(By.CSS_SELECTOR, self._source.css_search_link)
            for each in link:
                chap_text.append(each.text)
                chap_link.append(each.get_attribute('href'))
        elif self._model == 'Api':
            data = {self._source.search_key: key}
            if self._source.search_method == 'GET':
                response = requests.get(url=self._source.search_url, params=data, headers=self._headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                link = soup.select(self._source.search_rule)
                for each in link:
                    chap_text.append(each.text)
                    chap_link.append(each['href'])
        print('====================')
        print("name | url")
        for each in range(len(chap_text)):
            print(f'{chap_text[each]} | {chap_link[each]}'.replace(self._source.url, ''))
        print('====================')
        print('结束搜索')
        print('====================')

    def _read(self):
        print("====================")
        print("2.阅读")
        print("====================")
        url = input('请输入链接: ')
        if url == 'exit':
            return 0
        a = []
        if self._model == 'Selenium':
            self._browser.get(self._source.url + url)
            a = self._browser.find_elements(By.CSS_SELECTOR, self._source.css_chap_link)
        elif self._model == 'Api':
            response = requests.get(self._source.url + url, headers=self._headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            a = soup.select(self._source.catalo_rule)
        if len(a) == 0:
            print('Disable Chapter')
            return 0
        print('获取章节成功\n请注意，由于设计原因第一章可能不在序号 0')
        print(f'章节: {len(a)}')
        chap = input('请选择序号(q退出): ')
        if chap == 'q':
            return 0
        try:
            chap = int(chap)
        except BaseException:  # noqa
            chap = 0
        if chap < 0:
            chap = 0
        chapter_link = ''
        if self._model == 'Selenium':
            # self._browser.execute_script("arguments[0].click();", a[chap])
            chapter_link = a[chap].get_attribute('href')
        elif self._model == 'Api':
            chapter_link = a[chap]['href']
        if chapter_link == '':
            print('Disable Link')
            return 0
        if not re.match('http', chapter_link):
            chapter_link = self._source.url + chapter_link
        chapter_content = None
        chapter_next = None
        if self._model == 'Selenium':
            self._browser.get(chapter_link)
            p_list = self._browser.find_element(By.CSS_SELECTOR, self._source.css_content).text.splitlines()
            content = []
            for each in p_list:
                data = each.strip()
                if each == '':
                    continue
                else:
                    content.append(data)
            chapter_content = content
        elif self._model == 'Api':
            response = requests.get(chapter_link, headers=self._headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            chapter_next = soup.select(self._source.conten_next)[0]['href']
            p_list = soup.select(self._source.conten_rule)[0].find_all('p')
            content = []
            for each in p_list:
                data = each.text.strip()
                if data == '':
                    continue
                else:
                    content.append(data)
            if '免费阅读' in content[0]:
                content.pop(0)
            if '继续阅读' in content[-1]:
                content.pop(-1)
            chapter_content = content
        mirror_flag = 0
        while True:
            print("------------------------")
            count = 0
            for each in chapter_content:
                if mirror_flag == 1:
                    print(self._mirror(each))
                else:
                    print(each)
                count += 1
                if count == 5:
                    print("------------------------")
                    input_datax = input('继续打印(q退出): ')
                    if input_datax == 'q':
                        break
                    else:
                        if input_datax == 'm':  # mirror
                            mirror_flag = 1
                        elif input_datax == 'mc':  # mirror cance
                            mirror_flag = 0
                        count = 0
                    print("------------------------")
            if count != 5:
                print("------------------------")
            input_data = input('下一章(q退出): ')
            if input_data == 'q':
                break
            else:
                if input_data == 'm':  # mirror
                    mirror_flag = 1
                elif input_data == 'mc':  # mirror cance
                    mirror_flag = 0
                if self._model == 'Selenium':
                    element = self._browser.find_element(By.CSS_SELECTOR, self._source.css_next)
                    self._browser.execute_script("arguments[0].click();", element)
                    sleep(1)
                elif self._model == 'Api':
                    if not re.match('http', chapter_next):
                        chapter_link = self._source.url + chapter_next
                    response = requests.get(chapter_link, headers=self._headers)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    chapter_next = soup.select(self._source.conten_next)[0]['href']
                    p_list = soup.select(self._source.conten_rule)[0].find_all('p')
                    content = []
                    for each in p_list:
                        data = each.text.strip()
                        if data == '':
                            continue
                        else:
                            content.append(data)
                    if '免费阅读' in content[0]:
                        content.pop(0)
                    if '继续阅读' in content[-1]:
                        content.pop(-1)
                    chapter_content = content

    def _download(self):
        print("====================")
        print("3.下载")
        print("====================")
        result_file = './result'
        if not os.path.exists(result_file):
            os.mkdir(result_file)
        url = input('请输入链接: ')
        if url == 'exit':
            return 0
        self._browser.get(self._source.url + url)
        a = self._browser.find_elements(By.CSS_SELECTOR, self._source.css_chap_link)
        print('获取章节成功\n请注意，由于设计原因第一章可能不在序号 1')
        print(f'章节 {len(a)}')
        start = int(input('开始页：'))
        end = int(input('结束页：'))
        number = int(input('线程数：'))
        width = int((end - start) / number)
        t_start = start
        threads = []
        for each in range(number):
            if each == number - 1:
                t_end = end
            else:
                t_end = t_start + width
            print(f'线程分配：{t_start} to {t_end}')
            t = threading.Thread(target=self._get, args=(t_start, t_end, result_file, url))
            threads.append(t)
            t_start = t_end
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()

    def _get(self, start, end, result_file, url, browser):
        if browser == 1:
            _browser = Edge(service=Service(executable_path=self._edge_driver_path),
                            options=self._edge_options)
        else:
            _browser = Firefox(service=Service(executable_path=self._firefox_driver_path),
                               options=self._firefox_options)
        _browser.maximize_window()
        _browser.implicitly_wait(5)
        _browser.get(self._source.url + url)
        a = _browser.find_elements(By.CSS_SELECTOR, self._source.css_chap_link)
        _browser.execute_script("arguments[0].click();", a[start])
        while True:
            if end == start:
                break
            name = _browser.find_element(By.CSS_SELECTOR, self._source.css_content_name).text
            for each in ['\\', '/', ':', '*', '?', "\"", '<', '>', '|']:
                if each in name:
                    name = name.replace(each, '')
            with open(f'{result_file}/{start} = {name}.txt', 'wb') as f:
                content = _browser.find_element(By.CSS_SELECTOR, self._source.css_content).text.splitlines()
                for x in content:
                    if x == '':
                        continue
                    f.write(x.strip().encode('UTF-8'))
                    f.write('\n'.encode('UTF-8'))
            element = _browser.find_element(By.CSS_SELECTOR, self._source.css_next)
            _browser.execute_script("arguments[0].click();", element)
            print('.', end='')
            if start % 30 == 0:
                print('')
            start += 1
            sleep(2)
        print('线程关闭')

    def menu(self):
        print("====================")
        print("欢迎进入系统")
        print(self._source.message)
        if self._model not in ['Api', 'Selenium']:
            print('Disable Model')
            return 0
        print("====================")
        print('1.搜索')
        print('2.阅读')
        print('3.下载')
        print('6.退出')
        print("====================")
        while True:
            flag = input('请选择功能: ')
            if flag == '1':
                self._search()
            elif flag == '2':
                self._read()
            elif flag == '3':
                self._download()
            elif flag == '6':
                if self._model == 'Selenium':
                    self._browser.quit()
                break
            else:
                print('无此功能')
                continue
        print('退出系统')


if __name__ == '__main__':
    sour = ApiSource.yiqi_data
    Book(sour).menu()
