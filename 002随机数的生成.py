import random


# 练习一：生成一个前后数字完全不同的随机数
def random_different(length: int) -> int:
    current_length = 0
    last_num = None
    string = ''
    while current_length < length:
        temp = random.randint(0, 9)
        if current_length == 0:
            if temp != 0:
                string += str(temp)
                last_num = temp
                current_length += 1
                continue
        if temp != last_num:
            string = string + str(temp)
            last_num = temp
            current_length += 1
    return int(string)


print(random_different(10))


# 练习二：生成一个固定位数的随机数
def random_fixed(length: int) -> int:
    number = random.randint(10**(length-1), 10**length - 1)
    return number


print(random_fixed(10))


if __name__ == "__main__":
    pass
