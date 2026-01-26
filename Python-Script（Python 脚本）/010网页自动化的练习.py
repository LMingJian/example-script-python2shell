from time import sleep

import pytest
from selenium.webdriver import EdgeOptions, Edge
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

"""
A: 如何进行网页自动化测试
Selenium=4.1.0
"""


class TestClass:

    browser = None

    def setup_class(self):
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument('--disable-gpu')
        options.add_argument('window-size=1920x1080')
        options.add_argument('start-maximized')
        driver_path = r'F:\PythonProject\WebDrive\msedgedriver.exe'
        # 在 selenium4 中 executable_path 将不再支持，推荐使用 service
        self.browser = Edge(options=options, service=Service(executable_path=driver_path))

    @pytest.fixture(scope='function', autouse=True)
    def setup_teardown(self):
        self.browser.get("https://www.baidu.com")
        sleep(1)
        yield
        pass

    def teardown_class(self):
        self.browser.quit()

    def test_1(self):
        """百度搜索"""
        self.browser.find_element(By.ID, "kw").send_keys("selenium")
        self.browser.find_element(By.ID, "su").click()
        sleep(2)
        texts = self.browser.find_elements(By.XPATH, '//div/h3/a')
        # 循环遍历出每一条搜索结果的标题
        for t in texts:
            print(t.text)

    def test_2(self):
        """浏览器的后退"""
        self.browser.get("https://fanyi.baidu.com/")
        self.browser.back()
        print(self.browser.title)
        self.browser.refresh()

    def test_3(self):
        """鼠标的移动"""
        above = self.browser.find_element(By.LINK_TEXT, "更多")
        ActionChains(self.browser).move_to_element(above).perform()
        sleep(2)

    def test_4(self):
        """输入框的定位"""
        # noinspection PyBroadException
        try:
            self.browser.find_element(By.ID, "kw").send_keys("A")
            self.browser.find_element(By.CSS_SELECTOR, "s_ipt").send_keys("B")
            self.browser.find_element(By.NAME, "wd").send_keys("C")
            self.browser.find_element(By.XPATH, "//form[@id='form']/span/input").send_keys("D")
            self.browser.find_element(By.CSS_SELECTOR, "#su").click()
            self.browser.find_element(By.LINK_TEXT, "贴吧").click()
            print("Element OK")
        except BaseException as e:
            print(e)

    def test_5(self):
        """元素等待"""
        self.browser.get("https://www.baidu.com")
        locator = (By.ID, 'kw12')
        # "kw"时正常运行，”kw12“时出现超时异常，并不出现找不到元素的异常
        # noinspection PyBroadException
        try:
            element = WebDriverWait(self.browser, 5, 0.5).until(ec.presence_of_element_located(locator))
            element.send_keys("HELLO")
            sleep(2)
        except BaseException as e:
            print("Wait超时了")
            print(e)


if __name__ == "__main__":
    pytest.main(['-s'])
