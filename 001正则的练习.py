import re


def practice1():
    """
    Q: 匹配“这是某某的电话123456789，你可以打给他”中的电话号码
    A: 注意到这里是连续的数字匹配，同时又由于字段中无其他数字，因此可以使用 `sub` 函数匹配非数字内容并替换为空以实现电话号码提取
    正则: \\D, 匹配内容[^0-9], 即非0-9的内容
    re.sub(pattern, repString, string, count=0, flags=0): 将匹配到的内容进行替换
    """
    phone = re.sub(r'\D', "", "这是某某的电话123456789，你可以打给他")
    print(phone)


def practice2():
    """
    Q: 查看下match函数返回的内容
    A: match返回的是一个类，通过使用方法group(int)可以获取匹配到的字符串
    正则: \\d+, 匹配内容[0-9]+, 即至少匹配一个0-9的内容
    match(pattern, string, flags=0): 从头开始进行匹配，如果开头无法使用pattern匹配到，则会报错
    """
    m = re.match(r'\d+', '123=one, two, three=123')
    print(m)
    print(m.group(0))  # 用于获得一个或多个分组匹配结果的字符串
    print(m.start(0))  # 用于获取分组匹配的子串在整个字符串中的起始位置（子串第一个字符的索引）
    print(m.end(0))  # 用于获取分组匹配的子串在整个字符串中的结束位置（子串最后一个字符的索引+1）
    print(m.span(0))  # 返回(start(group), end(group))


def practice3():
    """
    Q: 获取”run 123 google 456 889、’11’、、PPT2“里的所有数字
    A: 使用findall匹配所有符合的内容
    正则: \\d+, 匹配内容[0-9]+, 即至少匹配一个0-9的内容
    findall(pattern, string, flags=0): 扫描整个字符串，找到所有符合的内容，返回的是字符串的列表
    """
    result = re.findall(r'\d+', 'run 123 google 456 889、’11、、2')
    print(result)


def practice4():
    """
    Q: 将”你好啊！（第三章)“中括号内的内容去除
    A: 可以先使用search对整个字符串进行匹配, 获取所有符合的内容，然后使用replace方法将括号内容去除
    正则: (（)(.*)(\\)), 匹配左边为（ , 右边为 ) 的内容
    search(pattern, string, flags=0): 扫描整个字符串查找与模式匹配的项，返回与match函数返回相同的类
    """
    string = '你好啊！（第三章)'
    result = re.search('(（)(.*)(\\))', string)
    print(result)
    print(result.group())
    string = string.replace(result.group(), '')
    print(string)


if __name__ == '__main__':
    flag = input('选择测试函数: ')
    if flag == '1':
        practice1()
    elif flag == '2':
        practice2()
    elif flag == '3':
        practice3()
    elif flag == '4':
        practice4()
    else:
        pass
