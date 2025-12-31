import base64
"""
Q: 如何实现base64编解码与凯撒加密
"""


def caesar(string, deviation):
    """
    A: 恺撒密码（英语：Caesar cipher），或称恺撒加密、恺撒变换、变换加密，是一种最简单且最广为人知的加密技术。
       它是一种替换加密的技术，明文中的所有字母都在字母表上向后（或向前）按照一个固定数目进行偏移后被替换成密文。
    """
    encryption = list(string)
    print("加密前")
    print(encryption)
    i = 0
    while i < len(encryption):
        if ord(encryption[i]) < 123 - deviation:
            encryption[i] = chr(ord(encryption[i]) + deviation)
        else:
            encryption[i] = chr(ord(encryption[i]) + deviation - 26)
        i = i + 1
    print("加密后")
    print(encryption)


def base(string):
    """
    A: base64编解码
    """
    # 编码
    encode_str = base64.encodebytes(string.encode('utf8'))
    print('编码前')
    print(encode_str.decode())
    # 解码
    decode_str = base64.decodebytes(encode_str)
    print('编码后')
    print(decode_str.decode())


if __name__ == "__main__":
    print("=============================")
    base('hello world!')
    print("=============================")
    caesar('test:test123', 6)
