from collections import deque


class A(object):
    pass


class B(A):
    pass


class C(A):
    pass


class D(B):
    pass


class E(D):
    pass


class Node(object):
    def __init__(self, data=None):
        self._data = data
        self._children = []

    def add_child(self, node):
        self._children.append(node)

    @property
    def children(self):
        return self._children

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data


class Tree(object):
    def __init__(self, root=None):
        self._root = root

    def walk(self, fn=deque.pop):
        stack = deque([(self._root, 0)])
        while stack:
            node, c_level = fn(stack)
            yield node, c_level
            stack.extend((node, c_level + 1) for node in node.children)


def get_all_classes(root_class):
    stack = [(root_class, 0)]
    while stack:
        clazz, c_level = stack.pop()
        yield clazz, c_level
        stack.extend((_cl, c_level + 1) for _cl in clazz.__subclasses__())


node = Node(1)
n3 = Node(3)
n3.add_child(Node(4))
node.add_child(Node(2))
node.add_child(n3)
node2 = Node(5)
node.children[0].add_child(node2)
node2.add_child(Node(7))


tree = Tree(node)
for _node, level in tree.walk(deque.popleft):
    print _node.get_data(), level
# for _class, level in get_all_classes(A):
#     print " " * level, _class.__name__