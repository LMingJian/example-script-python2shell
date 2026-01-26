"""
实现一个用于控制台，终端使用的系统菜单，可以无限循环
"""


def menu():
    while True:
        print('===============')
        print('欢迎进入系统')
        print('1.添加')
        print('2.删除')
        print('3.查找')
        print('4.修改')
        print('5.显示')
        print('6.退出')
        print('===============')
        function_key = input('请选择功能: ')
        if function_key == '1':
            pass
        elif function_key == '2':
            pass
        elif function_key == '3':
            pass
        elif function_key == '4':
            pass
        elif function_key == '5':
            pass
        elif function_key == '6':
            return 0
        else:
            print('抱歉，没有该功能')

if __name__ == '__main__':
    menu()