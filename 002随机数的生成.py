import random


def random1(length, start, end):
    """
    Q: 如何生成一个固定长度的随机数
    A: 首先随机生成一个数字，将数字转换为字符串，将字符串进行拼接就可以生成一个固定长度的随机数
    random.randint(start, end): 生成一个[start, end]的int型整数
    """
    string = ''
    for each in range(length):
        string = string+str(random.randint(start, end))
    return int(string)


def random2(length, start, end):
    """
    Q: 如何生成一个前后不一致的随机数
    A: 生成一个相邻数字不同的随机数，可以记录前一次生成的值，与下一次进行判断，相同则再生成一次
    """
    current_length = 0
    last_num = end + 1
    string = ''
    while current_length < length:
        flag = random.randint(start, end)
        if flag != last_num:
            string = string + str(flag)
            last_num = flag
            current_length += 1
    return int(string)


if __name__ == "__main__":
    temp = random1(10, 0, 5)
    print(temp)
    print(type(temp))
    temp = random2(10, 0, 5)
    print(temp)
    print(type(temp))


