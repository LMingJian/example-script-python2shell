import time

import pyperclip
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service


class ClipBoardListen:

    recent_txt = None

    @staticmethod
    def clipboard_get():
        """获取剪贴板数据"""
        return pyperclip.paste()

    def main(self):
        self.recent_txt = self.clipboard_get()
        while True:
            current_txt = self.clipboard_get()
            if current_txt != self.recent_txt:
                self.recent_txt = current_txt
                print(self.recent_txt)
            time.sleep(0.2)


class BingTranslate:

    _options = EdgeOptions()
    _options.use_chromium = True
    # _options.add_argument("headless")
    _options.add_argument('window-size=1920x1080')
    _options.add_argument('start-maximized')
    _driver_path = r'F:\PythonProject\WebDrive\msedgedriver.exe'
    recent_txt = None

    def __init__(self):
        self._browser = Edge(service=Service(executable_path=self._driver_path), options=self._options)
        self._browser.implicitly_wait(6)

    @staticmethod
    def clipboard_get():
        """获取剪贴板数据"""
        return pyperclip.paste()

    def test(self):
        self._browser.get('https://cn.bing.com/translator')
        print(self._browser.current_url)
        tta_input = self._browser.find_element(By.ID, 'tta_input_ta')
        self.recent_txt = self.clipboard_get()
        while True:
            current_txt = self.clipboard_get()
            if current_txt != self.recent_txt:
                self.recent_txt = current_txt
                tta_input.clear()
                tta_input.send_keys(self.recent_txt)
            time.sleep(0.2)


if __name__ == '__main__':
    BingTranslate().test()
