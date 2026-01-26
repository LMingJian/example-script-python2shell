import re
"""
A: 实现对XML文件的读取和创建
"""


class XmlBuilder:
    _processingText = ''
    _node = ''

    def processing(self, target, text):
        self._processingText = '<?{} {}?>'.format(target, text)

    def create_node(self, target, text):
        if isinstance(text, list):
            temp_string = ''
            for each in text:
                temp_string = temp_string + each
            self._node = '<{}>{}</{}>'.format(target, temp_string, target)
        else:
            self._node = '<{}>{}</{}>'.format(target, text, target)
        return self._node

    def make_xml(self, text):
        return self._processingText + text


class XmlReader:
    _xmlText = ''

    def __init__(self, text):
        self._xmlText = text.replace('\n', '')

    def read_xml(self, point):
        try:
            search = re.search('<{}>(.*)</{}>'.format(point, point), self._xmlText).group()
            return search.replace('<{}>'.format(point), '').replace('</{}>'.format(point), '')
        except BaseException as e:
            return str(e)


if __name__ == '__main__':
    """制作Xml字符串"""
    xml = XmlBuilder()
    xml.processing('xml', 'version="1.0" encoding="utf-8"')
    node = xml.create_node('root', [
        xml.create_node('name', [
            xml.create_node('xxx', 12),
            xml.create_node('ppp', 455)]),
        xml.create_node('age', 12),
        xml.create_node('school', 'School')])
    print(node)
    print(xml.make_xml(node))

    """读取Xml字符串"""
    string = """
<?xml version="1.0" encoding="UTF-8"?>
<response>
<lang>
<type>0</type>
<lan>Chinese</lan>
</lang>
</response>
    """
    x = XmlReader(string)
    print(x.read_xml('type'))
