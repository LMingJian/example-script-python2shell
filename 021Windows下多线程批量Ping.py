import subprocess
from threading import Thread

"""
Q: 如何使用Ping检查当前网段下可用IP
A: 简单方法是使用subprocess通过Python调用系统的Shell执行Ping
PS: 在下面的脚本中，由于使用了多线程，所以需要设置全局变量存储数据
"""
success = []
fail = []
error = []


class Pings(Thread):

    def __init__(self, ip):
        Thread.__init__(self)
        self.ip = ip

    def run(self):
        shell_request = subprocess.Popen('ping -n 1 %s' % self.ip, shell=True, stdout=subprocess.PIPE)
        shell_response = shell_request.communicate()[0].decode('GBK').split('\r\n')[2]
        if '无法访问' in shell_response:
            # print(f'{self.ip} : 无法访问Ip\n')
            fail.append(self.ip)
        elif 'TTL' in shell_response:
            # print(f'{self.ip} : 目标主机可以访问\n')
            success.append(self.ip)
        else:
            # print(f'{self.ip} : 请求超时\n')
            error.append(self.ip)


if __name__ == '__main__':
    host = ['192.168.1.1', '192.168.1.232', 'www.google.com']
    hostX = []
    for number in range(1, 256, 1):
        hostX.append(f'192.168.1.{number}')
    threads = []
    for each in host:
        threads.append(Pings(each))
    print('请等待执行.....')
    for each in threads:
        each.start()
    for each in threads:
        each.join()
    for each in success:
        print(f'允许访问IP: {each}')
