from collections import deque

list_numbers = [[], [[5,2,6], [[[[[8,4,8,3,8], 654]]], 9532]]]


def get_sum_recursive(numbers):
    nsum = 0
    for num in numbers:
        if isinstance(num, list):
            nsum += get_sum_recursive(num)
        else:
            nsum += num
    return nsum


def get_sum(numbers):
    nsum = 0
    stack = deque(numbers)
    while stack:
        num = stack.pop()
        if isinstance(num, list):
            stack.extend(num)
        else:
            nsum += num
    return nsum


recursive_sum = get_sum_recursive(list_numbers)
wo_rec = get_sum(list_numbers)
print recursive_sum, wo_rec, recursive_sum == wo_rec


                  #      ('c')
                  #      /   \
                  #    ('a', 'o')
                  #    /  \     \
                  #  ('t','r')  ('p')
                  #   /
                  #  ('egory')

class Node(object):
    def __init__(self, data, flag=False):
        self.data = data
        self.flag = flag
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        return child

    @staticmethod
    def walk(root):
        stack = deque([(root.data, root)])
        while stack:
            data, el = stack.popleft() # taking words from left ro right
            if not el.children:
                yield data
            else:
                for ch in el.children:
                    stack.append((data + ch.data, ch))
                if el.flag:
                    yield data


root = Node('c')
t = root.add_child(Node('a'))
root.add_child(Node('o')).add_child(Node('p'))
t.add_child(Node('t', True)).add_child(Node('egory'))
t.add_child(Node('r'))

print list(Node.walk(root))