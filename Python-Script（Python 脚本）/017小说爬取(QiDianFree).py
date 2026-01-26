import threading
from os import path, mkdir
from time import sleep

from selenium.webdriver import EdgeOptions, Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

"""
A: 使用浏览器, selenium4 实现的小说爬取。
   优点是不用解决网站权限验证的问题, 但爬取速度较慢。
   由于不知名原因, 使用无头浏览器时限免的Vip章节无法打印, 必须使用有头浏览器
"""


class QiDianFree:
    _baseUrl = 'https://www.qidian.com/free'
    _options = EdgeOptions()
    _options.use_chromium = True
    _options.add_argument("headless")
    _options.add_argument('window-size=1920x1080')
    _options.add_argument('start-maximized')
    _driver_path = r'F:\PythonProject\WebDrive\msedgedriver.exe'

    def __init__(self):
        self._browser = Edge(service=Service(executable_path=self._driver_path), options=self._options)
        self._browser.implicitly_wait(5)

    def search(self):
        print("====================")
        print('1.更新限免列表')
        print("====================")
        if_next = input('是否打印下期限免(q打印): ')
        self._browser.get(self._baseUrl)
        for each in self._browser.find_elements(By.CSS_SELECTOR, "#limit-list li h2 a"):
            print('----------------------')
            print(each.text)
            print(each.get_attribute('href'))
        if if_next == 'q':
            for each in self._browser.find_elements(By.CSS_SELECTOR, ".other-rec-wrap li h2 a"):
                print('----------------------')
                print(each.text)
                print(each.get_attribute('href'))
        print('----------------------')

    def read(self):
        print("====================")
        print("2.阅读")
        print("====================")
        string = input('请输入链接: ')
        self._browser.get(string)
        sleep(1)
        self._browser.find_element(By.CSS_SELECTOR, "#j_catalogPage").click()
        sleep(1)
        a = self._browser.find_elements(By.CSS_SELECTOR, "ul.cf li a")
        print('获取章节成功')
        print(len(a))
        chap = input('请选择章节(q退出): ')
        if chap == 'q':
            return 0
        try:
            chap = int(chap)
        except BaseException as e:
            print(e)
            print('跳转失败, 默认第一章')
            chap = 0
        self._browser.get(a[chap].get_attribute('href'))
        sleep(1)
        while True:
            print("------------------------")
            print(self._browser.find_element(By.CSS_SELECTOR, ".j_chapterName .content-wrap").text)
            print("------------------------")
            content = self._browser.find_elements(By.CSS_SELECTOR, ".j_readContent p .content-wrap")
            count = 0
            for each in content:
                print(each.text)
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
                self._browser.get(self._browser.find_element(By.CSS_SELECTOR, "#j_chapterNext").get_attribute('href'))
                sleep(1)

    def download(self):
        print("====================")
        print("3.下载")
        print("====================")
        result_file = './result'
        if not path.exists(result_file):
            mkdir(result_file)
        url = input('请输入链接: ')
        self._browser.get(url)
        sleep(1)
        self._browser.find_element(By.CSS_SELECTOR, "#j_catalogPage").click()
        sleep(1)
        a = self._browser.find_elements(By.CSS_SELECTOR, "ul.cf li a")
        print('获取章节成功')
        print(len(a))
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
            t = threading.Thread(target=self.get, args=(a, t_start, t_end, result_file))
            threads.append(t)
            t_start = t_end
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()

    def get(self, a, start, end, result_file):
        _browser = Edge(service=Service(executable_path=self._driver_path), options=self._options)
        try:
            _browser.get(a[start].get_attribute('href'))
        except BaseException as e:
            print(e)
            return 0
        sleep(1)
        while True:
            if end == start:
                break
            name = _browser.find_element(By.CSS_SELECTOR, ".j_chapterName .content-wrap").text
            for each in ['\\', '/', ':', '*', '?', "\"", '<', '>', '|']:
                if each in name:
                    name = name.replace(each, '')
            with open(f'{result_file}/{start} = {name}.txt', 'wb') as f:
                content = _browser.find_elements(By.CSS_SELECTOR, ".j_readContent p .content-wrap")
                for x in content:
                    f.write(x.text.encode('UTF-8'))
                    f.write('\n'.encode('UTF-8'))
            _browser.get(_browser.find_element(By.CSS_SELECTOR, "#j_chapterNext").get_attribute('href'))
            print('.', end='')
            if start % 30 == 0:
                print('')
            start += 1
            sleep(2)
        print('')

    def menu(self):
        print("====================")
        print("欢迎进入系统")
        print("====================")
        print('1.搜索')
        print('2.阅读')
        print('3.下载')
        print('6.退出')
        print("====================")
        while True:
            flag = input('请选择功能: ')
            if flag == '1':
                self.search()
            elif flag == '2':
                self.read()
            elif flag == '3':
                self.download()
            elif flag == '6':
                self._browser.quit()
                break
            else:
                print('无此功能')
                continue
        self._browser.quit()
        print('退出系统')


if __name__ == '__main__':
    QiDianFree().menu()
