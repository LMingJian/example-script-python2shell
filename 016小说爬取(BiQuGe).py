from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

"""
A: 使用无头浏览器, selenium4, BeautifulSoup实现的小说爬取。
   优点是不用解决网站权限验证的问题, 但爬取速度较慢
"""
"""
搜索服务不可用
"""


class BiQuGe:
    _baseUrl = 'https://www.biquwx.la'

    def __init__(self):
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument("headless")
        options.add_argument('window-size=1920x1080')
        options.add_argument('start-maximized')
        self._browser = webdriver.Remote(command_executor='http://192.168.127.137:4444',
                                         options=options)

    def search(self):
        print("====================")
        print("1.搜索")
        print("====================")
        key = input('请输入关键字: ')
        self._browser.get(self._baseUrl)
        sleep(1)
        element = self._browser.find_element(By.CSS_SELECTOR, "#wd")
        element.send_keys(key)
        element.send_keys(Keys.ENTER)
        sleep(1)
        page = self._browser.page_source
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find('table', class_='grid')
        soup = BeautifulSoup(str(table), 'html.parser')
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
        print('结束搜索')
        print('====================')

    def read(self):
        print("====================")
        print("2.阅读")
        print("====================")
        string = input('请输入链接: ')
        self._browser.get(self._baseUrl+string)
        sleep(1)
        a = self._browser.find_elements(By.CSS_SELECTOR, "#list dd a")
        print('获取章节成功')
        chap = input('请选择章节(q退出): ')
        if chap == 'q':
            return 0
        try:
            chap = int(chap)
        except BaseException as e:
            print(e)
            print('跳转失败, 默认第一章')
            chap = 0
        a[chap].click()
        sleep(1)
        while True:
            print("------------------------")
            print(self._browser.find_element(By.CSS_SELECTOR, ".bookname h1").text)
            print("------------------------")
            content = self._browser.find_element(By.CSS_SELECTOR, "#content").text.splitlines()
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
                self._browser.find_elements(By.CSS_SELECTOR, ".bottem a")[3].click()
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
                self.search()
            elif flag == '2':
                self.read()
            elif flag == '6':
                break
            else:
                print('无此功能')
                continue
        self._browser.quit()
        print('退出系统')


if __name__ == '__main__':
    BiQuGe().menu()
