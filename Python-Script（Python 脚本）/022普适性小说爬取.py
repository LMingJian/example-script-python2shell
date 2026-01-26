import os
from configparser import ConfigParser
from time import sleep

from selenium.webdriver import Edge, EdgeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

"""
如何使用
1.config_path = '022配置文件.ini' 中配置爬取 Url
2.根据变量名, 配置查询, 内容等的 CSS
"""


class ReadBook:

    browser = None
    config_path = '022配置文件.ini'
    url = None
    css_search = None
    css_search_link = None
    css_content_name = None
    css_content = None
    css_next = None

    def __init__(self):
        if os.path.exists(self.config_path):
            config = ConfigParser()
            config.read(self.config_path)
            driver_path = config.get('webdriver', 'path')
            driver_option = config.get('webdriver', 'option').split(',')
            options = EdgeOptions()
            for each in driver_option:
                options.add_argument(each.strip())
            self.browser = Edge(options=options,
                                service=Service(executable_path=driver_path))
            self.url = config.get('book', 'url')
            self.css_search = config.get('book', 'search_css')
            self.css_search_link = config.get('book', 'search_link_css')
            self.css_chap_link = config.get('book', 'chap_link_css')
            self.css_content_name = config.get('book', 'content_name_css')
            self.css_content = config.get('book', 'content_css')
            self.css_next = config.get('book', 'next_css')
        else:
            raise Exception('022配置文件.ini file does not exist')

    def test(self):
        self.browser.get('https://www.baidu.com')
        print(self.browser.current_url)

    def search(self):
        print("====================")
        print("1.搜索")
        print("====================")
        key = input('请输入关键字(exit-退出): ')
        if key == 'exit':
            return 0
        self.browser.get(self.url)
        sleep(1)
        element = self.browser.find_element(By.CSS_SELECTOR, self.css_search)
        element.send_keys(key)
        element.send_keys(Keys.ENTER)
        sleep(1)
        link = self.browser.find_elements(By.CSS_SELECTOR, self.css_search_link)
        chap_text = []
        chap_link = []
        for each in link:
            chap_text.append(each.text)
            chap_link.append(each.get_attribute('href'))
        print('====================')
        print("name | url")
        for each in range(len(chap_text)):
            print(f'{chap_text[each]} | {chap_link[each]}'.replace(self.url, ''))
        print('====================')
        print('结束搜索')
        print('====================')

    def read(self):
        print("====================")
        print("2.阅读")
        print("====================")
        string = input('请输入链接: ')
        if string == 'exit':
            return 0
        self.browser.get(self.url+string)
        sleep(1)
        a = self.browser.find_elements(By.CSS_SELECTOR, self.css_chap_link)
        print('获取章节成功\n请注意，由于设计原因第一章可能不在序号 1')
        print(f'章节 {len(a)}')
        chap = input('请选择序号(q退出): ')
        if chap == 'q':
            return 0
        try:
            chap = int(chap)
        except BaseException as e:
            print(e)
            print('跳转失败, 默认 1')
            chap = 0
        chap = chap - 1
        if chap <= 0:
            chap = 0
        self.browser.execute_script("arguments[0].click();", a[chap])
        sleep(3)
        while True:
            print("------------------------")
            print(self.browser.find_element(By.CSS_SELECTOR, self.css_content_name).text)
            print("------------------------")
            content = self.browser.find_element(By.CSS_SELECTOR, self.css_content).text.splitlines()
            count = 0
            for each in content:
                if each == '':
                    continue
                print(each.strip())
                count += 1
                if count == 5:
                    print("------------------------")
                    if input('继续打印(q退出): ') == 'q':
                        break
                    else:
                        count = 0
                    print("------------------------")
            if count != 5:
                print("------------------------")
            if input('下一章(q退出): ') == 'q':
                break
            else:
                element = self.browser.find_element(By.CSS_SELECTOR, self.css_next)
                self.browser.execute_script("arguments[0].click();", element)
                sleep(1)

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
                try:
                    self.search()
                except BaseException as e:
                    print(e)
                    print('系统错误')
            elif flag == '2':
                try:
                    self.read()
                except BaseException as e:
                    print(e)
                    print('系统错误')
            elif flag == '6':
                self.browser.quit()
                break
            elif flag == '0':
                self.test()
            else:
                print('无此功能')
                continue
        print('退出系统')


if __name__ == '__main__':
    ReadBook().menu()
