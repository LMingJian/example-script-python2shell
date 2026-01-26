import os
"""
将文件1的名字转换为文件2的名字
"""

file1 = open('A1.txt', 'r', encoding='utf-8')
a1 = file1.readlines()
file1.close()
file2 = open('A2.txt', 'r', encoding='utf-8')
a2 = file2.readlines()
file2.close()

for each in a1:
    try:
        os.rename(each.replace('\n', ''), a2[a1.index(each)].replace('\n', ''))
    except BaseException as e:
        print(e)
        continue
