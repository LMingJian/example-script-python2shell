import json
import time

import bs4
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Edge, EdgeOptions # noqa
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service


class DiYiBan:

    def __init__(self, driver_file, option):
        self.browser_driver = BrowserDriver('Firefox', option, driver_file)
        self.browser = self.browser_driver.open()
        # self.browser.install_addon(r".\040Borderify.zip", temporary=True)  # 自动化信息消除(异常)
        # self.browser.get('https://bot.sannysoft.com/')

    def close(self):
        self.browser.quit()

    def get_novel(self, url, ids):
        """
        ids: 章节 ID
        """
        self.browser.get(url)
        time.sleep(3)
        novel_author = self.browser.find_element(By.CSS_SELECTOR, '.info').text.split('\n')[0].replace('作者：', '')
        novel = self.browser.find_element(By.CSS_SELECTOR, '.chapter-list:nth-child(7)')
        novel_name = novel.find_element(By.CSS_SELECTOR, 'h4').text.replace('章节列表', '')
        chapter_tag = novel.find_elements(By.CSS_SELECTOR, 'li a')
        chapter_name = []
        for _ in chapter_tag:
            chapter_name.append(_.text)
        chapter_tag[ids].click()  # 点击章节跳转
        print(self.browser.current_url)
        time.sleep(6)
        page = len(self.browser.find_elements(By.CSS_SELECTOR, 'center.chapterPages a'))
        if page == 0:
            content_page = range(1)
        else:
            content_page = range(page)  # 分页
        content = []
        for _ in content_page:
            if len(self.browser.find_elements(By.CSS_SELECTOR, '#chapterinfo')) != 0:
                content_html = self.browser.find_element(By.CSS_SELECTOR, '#chapterinfo')
                content = self.content_decode(content_html.get_attribute("outerHTML"), 'chapterinfo')
            elif len(self.browser.find_elements(By.CSS_SELECTOR, '#ad')) != 0:
                content_html = self.browser.find_element(By.CSS_SELECTOR, '#ad')
                new_content = self.content_decode(content_html.get_attribute("outerHTML"), 'ad')
                content = content + new_content
            else:
                content_html = self.browser.find_element(By.CSS_SELECTOR, 'div.neirong')
                new_content = self.content_decode(content_html.get_attribute("outerHTML"), 'neirong', 'class')
                content = content + new_content
            if _+1 < len(content_page):
                self.browser.find_elements(By.CSS_SELECTOR, 'center.chapterPages a')[_+1].click()
                time.sleep(6)
        with open(f'./[{novel_author}] {novel_name}{ids}.txt', 'wb') as f:
            for _ in content:
                f.write(_.encode('UTF-8'))
                f.write('\n\n'.encode('UTF-8'))

    def content_decode(self, content_html, target, target_type='id'):
        content = []
        content_temp = ''
        if target != '':
            soup = BeautifulSoup(content_html, 'html.parser')
            if target_type == 'class':
                div = soup.find('div', class_=target)
            else:
                div = soup.find('div', id=target)
        else:
            div = content_html
        for _ in div:
            if isinstance(_, bs4.element.NavigableString):
                content_temp = content_temp + _.strip()
            elif _.name == 'br':
                if (content_temp not in content) and (content_temp != ''):
                    content.append(content_temp)
                    content_temp = ''
            elif _.name == 'img':
                img_id = _.get('src').replace('/toimg/data/', '')
                content_temp = content_temp + self.img_texts_reverse(img_id)
            elif _.name == 'i':
                iconfont = _.contents[0]
                icon_id = repr(iconfont).replace(r"\ue", "").replace('\'', '')
                content_temp = content_temp + self.icon_texts_reverse(icon_id)
            elif _.name == 'div':
                content = content + self.content_decode(_, '')
        if (content_temp not in content) and (content_temp != ''):
            content.append(content_temp)
        return content

    @staticmethod
    def img_texts_reverse(img_id):
        json_file = './040Replace.json'
        with open(json_file, 'r', encoding='UTF-8') as file:
            json_data = json.load(file)['texts']
        if img_id in json_data:
            return json_data[img_id]
        else:
            return f"[{img_id}]"

    @staticmethod
    def icon_texts_reverse(icon_id):
        json_file = './040ReplaceIconFont.json'
        with open(json_file, 'r', encoding='UTF-8') as file:
            json_data = json.load(file)['texts']
        if icon_id in json_data:
            return json_data[icon_id]
        else:
            return f"[{icon_id}]"

    def get_novel_list(self, base_url, cookie_name, cookie_value, start_page=1):
        print('------------------')
        url = base_url+f'shuku/0-lastupdate-0-{start_page}.html'
        cookie = {'name': f'{cookie_name}', 'value': f'{cookie_value}'}
        self.browser.get(url)
        self.browser.add_cookie(cookie)
        self.browser.get(url)
        time.sleep(5)
        novel = self.browser.find_elements(By.CSS_SELECTOR, 'li.column-2 a.name')
        for each in novel:
            novel_name = each.text
            novel_link = each.get_attribute('href').replace(base_url, '')
            print(novel_name)
            print(novel_link)
            print('------------------')
        if_next = input('Next：')
        while if_next != 'q':
            print('Go Next')
            self.browser.find_element(By.CSS_SELECTOR, 'a.nextPage').click()
            time.sleep(5)
            print('------------------')
            novel = self.browser.find_elements(By.CSS_SELECTOR, 'li.column-2 a.name')
            for each in novel:
                novel_name = each.text
                novel_link = each.get_attribute('href').replace(base_url, '')
                print(novel_name)
                print(novel_link)
                print('------------------')
            if_next = input('Next：')
            time.sleep(1)
        return 0

    def manual(self):
        while True:
            flag = input('Are you ready?(get novel detail): ')
            if flag == 'n':
                return 0
            content = []
            while True:
                print(self.browser.current_url)
                if len(self.browser.find_elements(By.CSS_SELECTOR, '#chapterinfo')) != 0:
                    content_html = self.browser.find_element(By.CSS_SELECTOR, '#chapterinfo')
                    content = content + self.content_decode(content_html.get_attribute("outerHTML"), 'chapterinfo')
                elif len(self.browser.find_elements(By.CSS_SELECTOR, '#ad')) != 0:
                    content_html = self.browser.find_element(By.CSS_SELECTOR, '#ad')
                    new_content = self.content_decode(content_html.get_attribute("outerHTML"), 'ad')
                    content = content + new_content
                else:
                    content_html = self.browser.find_element(By.CSS_SELECTOR, 'div.neirong')
                    new_content = self.content_decode(content_html.get_attribute("outerHTML"), 'neirong', 'class')
                    content = content + new_content
                flag = input('Next Page?: ')
                if flag == 'n':
                    break
            with open(f'./[] {time.time()}.txt', 'wb') as f:
                for _ in content:
                    f.write(_.encode('UTF-8'))
                    f.write('\n\n'.encode('UTF-8'))
            print('Write Complete')


class BrowserDriver:
    """
    调用 open 方法，启动浏览器
    """

    def __init__(self, browser_name, options, dirve_file):
        self.browser_name = browser_name
        self.options = options
        self.dirve_file = dirve_file
        self._browser = None

    def open(self):
        if self.browser_name == "Firefox":
            self._browser = self._firefox()
            self._browser.maximize_window()
            return self._browser
        elif self.browser_name == "Chrome":
            self._browser = self._chrome()
            self._browser.maximize_window()
            return self._browser
        elif self.browser_name == "Edge":
            self._browser = self._edge()
            self._browser.maximize_window()
            return self._browser

    def test(self):
        browser = self.open()
        browser.get("https://www.baidu.com/")
        print(browser.current_url)
        time.sleep(2)
        browser.quit()

    def _edge(self):
        driver_path = rf"{self.dirve_file}\msedgedriver.exe"
        options = EdgeOptions()
        for each in self.options:
            if each:
                options.add_argument(each)
        browser = Edge(service=Service(executable_path=driver_path), options=options)
        browser.implicitly_wait(5)
        browser.maximize_window()
        return browser

    def _chrome(self):
        driver_path = rf"{self.dirve_file}\chromedriver.exe"
        options = ChromeOptions()
        for each in self.options:
            if each:
                options.add_argument(each)
        browser = Chrome(service=Service(executable_path=driver_path), options=options)
        browser.implicitly_wait(5)
        browser.maximize_window()
        return browser

    def _firefox(self):
        driver_path = fr"{self.dirve_file}\geckodriver.exe"
        options = FirefoxOptions()
        for each in self.options:
            if each:
                options.add_argument(each)
        browser = Firefox(service=Service(executable_path=driver_path), options=options)
        browser.implicitly_wait(5)
        browser.maximize_window()
        return browser


if __name__ == "__main__":
    dirve_file_path = r"D:\SDK\webdrive"
    func = input('Function: ')
    if func == 't':
        """测试"""
        b = BrowserDriver('Firefox', [], dirve_file_path)
        b.test()
    elif func == 'm':
        """手动爬取"""
        diyiban = DiYiBan(dirve_file_path, [])
        diyiban.manual()
        diyiban.close()
    elif func == '1':
        """正文"""
        diyiban = DiYiBan(dirve_file_path, ['-headless'])
        for x in range(7):
            diyiban.get_novel('url', x)
            time.sleep(3)
        diyiban.close()
    elif func == '2':
        """书籍列表"""
        diyiban = DiYiBan(dirve_file_path, ['-headless'])
        diyiban.get_novel_list('url', '__cf_bm', 'cookie')
        diyiban.close()
    print('System End')
