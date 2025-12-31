from time import sleep

from selenium import webdriver


def electron_selenium(software):
    options = webdriver.ChromeOptions()
    options.binary_location = software
    driver = webdriver.Chrome(options=options, executable_path=r'F:\PythonProject\WebDrive\chromedriver.exe')
    sleep(5)
    # t = driver.find_elements_by_css_selector(".el-input")
    # t[0].send_keys('123456')
    # t[1].send_keys('123456')
    # sleep(3)
    # driver.find_element_by_css_selector(".submit-item button").click()
    sleep(10)
    driver.quit()


if __name__ == "__main__":
    electron_software = ''
    # 软件的路径
    electron_selenium(electron_software)


