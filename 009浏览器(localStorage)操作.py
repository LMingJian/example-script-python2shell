from time import sleep

from selenium.webdriver import EdgeOptions, Edge
from selenium.webdriver.edge.service import Service

"""
pip install selenium >= 4
"""


def start_browser():
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument('--disable-gpu')
    options.add_argument('window-size=1920x1080')
    options.add_argument('start-maximized')
    driver_path = r'F:\PythonProject\WebDrive\msedgedriver.exe'
    # 在 selenium4 中 executable_path 将不再支持，推荐使用 service
    return Edge(options=options, service=Service(executable_path=driver_path))


def set_local_storage(string):
    """
    Q: 如何使用selenium实现对浏览器localStorage的操作
    A: 使用execute_script函数在控制台使用js实现操作
    """
    script = "localStorage.setItem({})".format(string)
    browser.execute_script(script)


def clear_local_storage():
    script = "localStorage.clear()"
    browser.execute_script(script)


if __name__ == "__main__":
    browser = start_browser()
    browser.get("https://www.baidu.com/")
    sleep(1)
    set_local_storage("'user', 'admin'")
