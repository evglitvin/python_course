from collections import deque


class Node(object):
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def add_child(self, child):
        if self.data > child.data:
            self.left = child
        else:
            self.right = child
        return child

    @staticmethod
    def walk(root):
        stack = deque([root])
        res_list = deque([root])
        while stack:
            el = stack.pop()

            if el.left:
                res_list.appendleft(el.left)
                stack.appendleft(el.left)

            if el.right:
                res_list.append(el.right)
                stack.append(el.right)
        return res_list

t = Node(8)
t.add_child(Node(6))
t.add_child(Node(10)).add_child(Node(20))

print [i.data for i in Node.walk(t)]

