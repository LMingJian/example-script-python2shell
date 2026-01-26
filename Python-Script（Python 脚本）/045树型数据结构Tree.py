class TreeNode:
    def __init__(self, data, name=None, uid=None):
        self.data = data  # 节点存储的数据
        self.name = name
        self.uid = uid
        self.parent = None  # 父节点指针（新增）
        self.children = []  # 存储子节点的列表
        self.has_child = False

    def add_child(self, child_node):
        """添加子节点并设置父节点"""
        child_node.parent = self  # 关键设置，将自己设置为父节点
        self.children.append(child_node)

    def find_node(self, target_data):
        """查找指定数据的节点"""
        if self.data == target_data:
            return self

        for child in self.children:
            found = child.find_node(target_data)
            if found:
                return found
        return None

    def find_node_name(self, target_name):
        """查找指定数据的节点"""
        if self.name == target_name:
            return self

        for child in self.children:
            found = child.find_node_name(target_name)
            if found:
                return found
        return None

    def remove_child(self, target):
        """删除子节点"""
        # 支持按节点对象或节点数据删除
        targets = [child for child in self.children
                   if child == target or child.data == target]

        if not targets:
            return False

        for child in targets:
            child.parent = None  # 清除父节点关联
            self.children.remove(child)
        return True

    def get_path(self):
        """获取从根节点到当前节点的路径"""
        path = []
        current = self
        while current:
            path.insert(0, current.data)
            current = current.parent
        return '->'.join(path)

    def __repr__(self, level=0):
        """增强可视化显示父节点信息"""
        parent_info = f" (parent: {self.parent.data})" if self.parent else ""
        ret = "\t" * level + f"|-- {self.data}{parent_info}\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret


# 使用示例
if __name__ == "__main__":
    root = TreeNode("A")
    root.add_child(TreeNode("B"))
    root.add_child(TreeNode("C"))
    node = TreeNode("D")
    root.add_child(node)
    node.add_child(TreeNode("E"))

    print("原始结构")
    print(root)

    print("查找节点 E")
    res = root.find_node("E")
    print(f"找到节点: {res.data}, 路径: {res.get_path()}")

    print("删除节点 E")
    node.remove_child("E")
    print(root)

    print("尝试查找已删除的 F")
    print(f"查找结果: {root.find_node('E')}")

    print("\n查看节点 B 的路径")
    print(root.children[0].get_path())
