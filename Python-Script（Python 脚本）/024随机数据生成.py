import random


class FakeData:
    """
    假数据
    """
    _second_name_list = [
        '秀', '娟', '英', '华', '慧', '巧', '美', '娜', '静', '淑', '惠', '珠', '翠', '雅', '芝', '玉', '萍', '红', '娥', '玲',
        '芬', '芳', '燕', '彩', '春', '菊', '兰', '凤', '洁', '梅', '琳', '素', '云', '莲', '真', '环', '雪', '荣', '爱', '畅',
        '霞', '香', '月', '莺', '媛', '艳', '瑞', '凡', '佳', '嘉', '琼', '勤', '珍', '贞', '莉', '桂', '娣', '叶', '璧', '璐',
        '娅', '琦', '晶', '妍', '茜', '秋', '珊', '莎', '锦', '黛', '青', '倩', '婷', '姣', '婉', '娴', '瑾', '颖', '露', '瑶',
        '怡', '婵', '雁', '蓓', '纨', '仪', '荷', '丹', '蓉', '眉', '君', '琴', '蕊', '薇', '菁', '梦', '岚', '苑', '婕', '馨',
        '瑗', '琰', '韵', '融', '园', '艺', '咏', '卿', '聪', '澜', '纯', '毓', '悦', '昭', '冰', '爽', '琬', '茗', '羽', '希',
        '宁', '欣', '飘', '育', '滢', '馥', '筠', '柔', '竹', '霭', '凝', '晓', '欢', '霄', '枫', '芸', '菲', '寒', '伊', '亚',
        '宜', '可', '姬', '舒', '影', '荔', '枝', '思', '丽', '伟', '刚', '勇', '毅', '俊', '峰', '强', '军', '平', '保', '东',
        '文', '辉', '力', '明', '永', '健', '世', '广', '志', '义', '兴', '良', '海', '山', '仁', '波', '宁', '贵', '福', '生',
        '龙', '元', '全', '国', '胜', '学', '祥', '才', '发', '武', '新', '利', '清', '飞', '彬', '富', '顺', '信', '子', '杰',
        '涛', '昌', '成', '康', '星', '光', '天', '达', '安', '岩', '中', '茂', '进', '林', '有', '坚', '和', '彪', '博', '诚',
        '先', '敬', '震', '振', '壮', '会', '思', '群', '豪', '心', '邦', '承', '乐', '绍', '功', '松', '善', '厚', '庆', '磊',
        '民', '友', '裕', '河', '哲', '江', '超', '浩', '亮', '政', '谦', '亨', '奇', '固', '之', '轮', '翰', '朗', '伯', '宏',
        '言', '若', '鸣', '朋', '斌', '梁', '栋', '维', '启', '克', '伦', '翔', '旭', '鹏', '泽', '晨', '辰', '士', '以', '建',
        '家', '致', '树', '炎', '德', '行', '时', '泰', '盛', '雄', '琛', '钧', '冠', '策', '腾', '楠', '榕', '风', '航', '弘']
    _first_name_list = [
        '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
        '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
        '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
        '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
        '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
        '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
        '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']
    _city = ['广州市']
    _jurisdiction = ['荔湾区', '越秀区', '海珠区', '天河区', '白云区', '黄埔区', '番禺区', '花都区', '南沙区', '从化区', '增城区']
    _school = ['第一中学', '第二中学', '实验中学']

    def _second_name(self):  # 随机取名
        number = random.randint(0, len(self._second_name_list) - 1)
        return self._second_name_list[number]

    def _first_name(self):  # 随机取姓
        number = random.randint(0, len(self._first_name_list) - 1)
        return self._first_name_list[number]

    def create_name(self):
        """创建假名字"""
        number = random.randint(1, 2)
        name = ''
        for i in range(number):
            name = name + self._second_name()
        return self._first_name() + name

    def create_school(self):
        """创建假学校"""
        number1 = random.randint(0, len(self._jurisdiction) - 1)
        number2 = random.randint(0, len(self._school) - 1)
        school = self._jurisdiction[number1].replace('区', self._school[number2])
        return school

    @staticmethod
    def create_id4(base, number):
        """
        创建符合规格的ID,最大9999,规格：base+四位序号（ 0001 ）
        :param base: id前缀
        :param number: 后缀序号
        :return: 字符串
        """
        if type(number) != int:
            return 'error input'
        if number <= 0:
            return 'Number not 0 or negative'
        base = str(base)
        if number < 10:
            return base + f'000{number}'
        elif number < 100:
            return base + f'00{number}'
        elif number < 1000:
            return base + f'0{number}'
        elif number >= 10000:
            return 'Limit exceeded'
        else:
            return base + f'{number}'

    @staticmethod
    def create_id3(base, number):
        """
        创建符合规格的ID,最大999,规格：base+三位序号（ 001 ）
        :param base: id前缀
        :param number: 后缀序号
        :return: 字符串
        """
        if type(number) != int:
            return 'error input'
        if number <= 0:
            return 'Number not 0 or negative'
        base = str(base)
        if number < 10:
            return base + f'00{number}'
        elif number < 100:
            return base + f'0{number}'
        elif number < 1000:
            return base + f'{number}'
        elif number >= 1000:
            return 'Limit exceeded'

    @staticmethod
    def create_phone():
        return '12345678910'

    @staticmethod
    def create_mail():
        flag = random.randint(1, 2)
        if flag == 1:
            return '123456789@qq.com'
        elif flag == 2:
            return '123456789@163.com'


if __name__ == "__main__":
    fake = FakeData()
    print(fake.create_school())
