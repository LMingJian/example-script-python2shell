from time import sleep

import pytest
import requests

"""
执行 pytest.main() 
注意，在 PyCharm 中执行 if __name__ == "__main__"，修改运行配置，在实参中添加参数 -n 3 启动多线程
注意，在 PyCharm 中如果脚本被判断为 Pytest，则主函数中的内容不会被执行
"""

ips = ['https://cn.bing.com/', 'https://www.baidu.com/', 'https://fanyi.baidu.com/']


@pytest.fixture(params=ips)
def data(request):
    yield request.param


def test_04(data):
    response = requests.get(url=data)
    sleep(5)
    print(f'数据：{data}, {response}')
    print('豪华')


if __name__ == "__main__":
    pytest.main(['-n', '3'])
