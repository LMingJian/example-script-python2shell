import telnetlib
"""
Q: 如何使用telnet远程登录Linux系统
"""


def telnets(host, user, password):
    # 登录
    tn = telnetlib.Telnet(host)
    tn.read_until(b"login: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

    # 命令
    tn.write(b"ls\n")
    tn.write(b"cd ..\n")
    tn.write(b"exit\n")

    # 打印结果
    result = tn.read_all().decode('ascii')
    print(result)


if __name__ == "__main__":
    telnets('IP', 'username', 'password')
