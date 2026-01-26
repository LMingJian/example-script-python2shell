from os import path, mkdir, listdir
from time import strftime


if __name__ == "__main__":
    """
    Q: 如何获取当前文件路径
    """
    cur_path = path.dirname(path.realpath(__file__))
    print('====================')
    print(cur_path)
    print('====================')

    """
    Q: 如何判断某个文件是否存在
    """
    ifExist = path.exists('./report')
    print(ifExist)
    print('====================')

    """
    Q: 如何对路径进行拼接
    """
    result = path.join(cur_path, "report")
    print(result)
    print('====================')

    """
    Q: 如何获取当前的时间
    """
    now = strftime("%Y.%m.%d[%H:%M:%S]")
    print(now)
    print('====================')

    """
    Q: 如何判断文件夹存在并创建文件夹
    """
    result = './report'
    if not path.exists(result):
        mkdir(result)

    """
    Q: 如何打印文件夹内所有文件的列表
    """
    dirs = listdir('./')
    print(dirs)
