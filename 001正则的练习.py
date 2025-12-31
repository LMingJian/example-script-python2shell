import re


# 练习一：提取所有手机号
def re_phone_numbers(text: str) -> list:
    # 定义匹配手机号码的正则表达式
    pattern = r'1[3-9]\d{9}'
    # 使用 re.findall 提取所有匹配的手机号码
    # findall 返回是一个列表
    phone_numbers = re.findall(pattern, text)
    return phone_numbers


for each in re_phone_numbers('我的手机号码是13812345678,不是12345678901'):
    print(each)


# 练习二：提取所有邮箱
def re_emails(text: str) -> list:
    # 定义匹配邮箱的正则表达式
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # 使用 re.findall 提取所有匹配的邮箱
    # findall 返回是一个列表
    emails = re.findall(pattern, text)
    return emails


for each in re_emails('我的邮箱是 example@qq.com 或者 example@163.org'):
    print(each)


# 练习三：清理 Windows 文件名
def re_clean_filename(text: str) -> str:
    # 替换所有 Windows 文件名非法字符 <>:"/\|?*
    pattern = r'[<>:"/\\|?*]'
    filename = re.sub(pattern, '', text)
    return filename


print(re_clean_filename('文/件>夹\\'))


# 练习四：搜索数据是否以特定字符开头
def re_check_header(text: str, header: str) -> bool:
    if re.match(header, text):
        return True
    else:
        return False


check_header = '139134'
print(re_check_header(check_header, '139'))
print(re_check_header(check_header, '134'))


# 练习五：搜索数据中是否存在特定字符
def re_check_number(text: str, number: str) -> bool:
    if re.search(number, text):
        return True
    else:
        return False


check_number = '139134'
print(re_check_number(check_number, '139'))
print(re_check_number(check_number, '134'))


if __name__ == '__main__':
    pass
