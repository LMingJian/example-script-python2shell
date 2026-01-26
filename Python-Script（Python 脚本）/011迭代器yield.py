"""
Q: yield是什么
A: yield是一个迭代器，当函数执行到yield时，会先返回yield后的内容，然后暂停函数剩下的执行，直到函数被next()唤起
"""


def gen():
    print("starting...")
    while True:
        yield 5
        # 返回5，等待next()下一步执行
        res = yield 4
        # 返回4后程序便被截断了，res无接收到值，next()执行后会执行到下一个yield
        print("res:", res)


if __name__ == "__main__":
    g = gen()
    print('第一次执行----------')
    print(next(g))
    print('第二次执行----------')
    print(next(g))
    print('第三次执行----------')
    print(next(g))
