"""
Q: 实现一个简单的学生管理系统，能对学生的信息进行增删查改
A: 实现对学生信息的增删查改，退出程序不保存信息。使用控制台展示信息
PS: 如要保存信息，可以使用file.write()的方法将结果写入文件以进行保存或恢复
"""


def check_input_number(string):
    while True:
        try:
            return int(input(string))
        except BaseException as e:
            print('输入格式错误，仅允许输入数字！')
            print(e)


class School:
    grades = ''
    classes = ''


class Student(School):
    name = ''
    number = ''

    def __init__(self):
        print('===============')
        print('  1.添加')
        print('===============')
        self.name = input('姓名:')
        self.number = check_input_number('学号: ')
        self.grades = check_input_number('年级(1-7年级): ')
        while self.grades not in range(1, 8):
            print('没有该年级')
            self.grades = check_input_number('年级(1-7年级): ')
        self.classes = check_input_number('班级(1-10班): ')
        while self.classes not in range(1, 11):
            print('没有该班级')
            self.classes = check_input_number('班级(1-10班): ')
        print('===============')
        print('添加成功')
        print('===============')

    def show(self):
        print(self.grades, end=' | ')
        print(self.classes, end=' | ')
        print(self.name, end=' | ')
        print(self.number)
        print('----------------')

    def check_num(self, number):
        if self.number == number:
            return 1
        else:
            return 0

    def revise(self):
        print('请选择修改的内容, 置空不修改')
        name = input('姓名: ')
        if name:
            self.name = name
        while True:
            grades = input('年级(1-7年级): ')
            if grades:
                try:
                    if int(grades) not in range(1, 8):
                        print('没有该年级')
                    else:
                        self.grades = int(grades)
                        break
                except BaseException as e:
                    print('输入格式错误，仅允许输入数字！')
                    print(e)
            else:
                break
        while True:
            classes = input('班级(1-10班): ')
            if classes:
                try:
                    if int(classes) not in range(1, 11):
                        print('没有该班级')
                    else:
                        self.classes = int(classes)
                        break
                except BaseException as e:
                    print('输入格式错误，仅允许输入数字！')
                    print(e)
            else:
                break
        print('===============')
        print('修改成功')
        print('===============')


# 如果需要管理老师，可以仿造Student编写类，并在System增加相应入口
class Teacher(School):
    name = ''
    number = ''


class System:
    studentList = []
    functionKey = 0

    def start(self):
        while True:
            print('===============')
            print('欢迎进入学生管理系统')
            print('  1.添加')
            print('  2.删除')
            print('  3.查找')
            print('  4.修改')
            print('  5.显示')
            print('  6.退出')
            print('===============')
            self.functionKey = check_input_number('请选择功能: ')
            if self.functionKey == 1:
                self.add()
            elif self.functionKey == 2:
                self.delete()
            elif self.functionKey == 3:
                self.search()
            elif self.functionKey == 4:
                self.revise()
            elif self.functionKey == 5:
                self.display()
            elif self.functionKey == 6:
                return 0
            else:
                print('抱歉，没有该功能')

    def add(self):
        self.studentList.append(Student())

    def delete(self):
        if self.studentList:
            print('===============')
            print('  2.删除')
            print('===============')
            number = check_input_number('请输入删除学生的学号: ')
            for each in self.studentList:
                if each.check_num(number):
                    self.studentList.remove(each)
                    del each
                    print('===============')
                    print('删除完成')
                    print('===============')
                    return 0
                else:
                    continue
            print('===============')
            print('没有该学号学生')
            print('===============')
        else:
            print('抱歉，查找不到数据')

    def search(self):
        if self.studentList:
            print('===============')
            print('  3.查找')
            print('===============')
            number = check_input_number('请输入查找学生的学号: ')
            for each in self.studentList:
                if each.check_num(number):
                    print('年级', end=' | ')
                    print('班级', end=' | ')
                    print('姓名', end=' | ')
                    print('学号')
                    each.show()
                    print('打印完毕')
                    print('----------------')
                    return 0
                else:
                    continue
            print('===============')
            print('没有该学号学生')
            print('===============')
        else:
            print('抱歉，查找不到数据')

    def revise(self):
        if self.studentList:
            print('===============')
            print('  4.修改')
            print('===============')
            number = check_input_number('请输入修改学生的学号: ')
            for each in self.studentList:
                if each.check_num(number):
                    each.revise()
                    return 0
                else:
                    continue
            print('===============')
            print('没有该学号学生')
            print('===============')
        else:
            print('抱歉，查找不到数据')

    def display(self):
        if self.studentList:
            print('===============')
            print('  5.显示')
            print('===============')
            print('年级', end=' | ')
            print('班级', end=' | ')
            print('姓名', end=' | ')
            print('学号')
            for each in self.studentList:
                each.show()
            print('打印完毕')
            print('----------------')
        else:
            print('抱歉，查找不到数据')


if __name__ == "__main__":
    System().start()
