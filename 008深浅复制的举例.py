import copy


def deep_copy():
    """
    Q: 什么是浅复制
    A: 使用 copy.deepcopy() 的是深复制, 深复制不复制物理地址, 即复制体与本体不使用同一个值, 使用不同物理地址ID;
       对本体或复制体修改, 不会影响复制体或本体的值
    """
    print('---------深复制-----------')
    will = ["Will", 28, ["Python", "C#", "JavaScript"]]
    will1 = copy.deepcopy(will)
    print('本体地址ID')
    print(id(will))
    print(will)
    print([id(ele) for ele in will])
    print('------------------------')
    print('复制体地址ID')
    print(id(will1))
    print(will1)
    print([id(ele) for ele in will1])
    print('-------深复制的修改--------')
    will1[0] = "Wills"
    will1[2].append("C++")
    print('修改后本体的值')
    print(id(will))
    print(will)
    print([id(ele) for ele in will])
    print('------------------------')
    print('修改后复制体的值')
    print(id(will1))
    print(will1)
    print([id(ele) for ele in will1])


deep_copy()


def shallow_copy():
    """
    Q: 什么是浅复制
    A: 形如 flag1 = flag 的是浅复制, 浅复制复制物理地址, 即复制体与本体使用同一个值, 同一个物理地址ID;
       对本体或复制体修改, 同时也会修改复制体或本体的值
    """
    print('---------浅复制-----------')
    will = ["Will", 28, ["Python", "C#", "JavaScript"]]
    will1 = will
    print('本体地址ID')
    print(id(will))
    print(will)
    print([id(ele) for ele in will])
    print('------------------------')
    print('复制体地址ID')
    print(id(will1))
    print(will1)
    print([id(ele) for ele in will1])
    print('-------浅复制的修改--------')
    will1[0] = "Wills"
    will1[2].append("C++")
    print('修改后本体的值')
    print(id(will))
    print(will)
    print([id(ele) for ele in will])
    print('------------------------')
    print('修改后复制体的值')
    print(id(will1))
    print(will1)
    print([id(ele) for ele in will1])


shallow_copy()


if __name__ == "__main__":
    pass
