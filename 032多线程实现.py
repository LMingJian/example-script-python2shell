import threading
from time import ctime, sleep

import requests

ips = ['https://cn.bing.com/', 'https://www.baidu.com/', 'https://fanyi.baidu.com/']


def get(data):
    print(ctime())
    response = requests.get(url=data)
    sleep(100)
    print(f'数据：{data}, {response}, {ctime()}')


if __name__ == '__main__':
    threads = []
    for each in ips:
        t1 = threading.Thread(target=get, args=(each, ))
        threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    """
    # 使用 while 卡住主程序，等待子线程执行执行
    while True:
        sleep(5)
        print(threading.active_count())
        if threading.active_count() == 1:
            sleep(10)
            break
    """
