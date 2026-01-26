import time

from selenium import webdriver

"""
服务端
下载 selenium-server 文件在服务端处
https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.1.0/selenium-server-4.1.1.jar
配置 java 环境
配置 webdriver 路径（webdriver必须在系统路径中，以便于服务端能定位）
执行 java -jar selenium-server-<version>.jar standalone 启动
"""


"""
客户端
"""
edge_options = webdriver.EdgeOptions()
driver = webdriver.Remote(
    command_executor='http://192.168.127.137:4444',
    # 可以直接访问 http://192.168.127.137:4444 进入简单的 selenium 查看界面
    options=edge_options
)
driver.get("http://www.baidu.com")
time.sleep(10)
driver.quit()
