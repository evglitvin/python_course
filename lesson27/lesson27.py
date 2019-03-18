

# list | | | | | | | | |
# list[5]
#
# 5 * 4 = 20
# 0xff4590 + 20
#
# void *c = malloc(200)
#
# c = 0xff4590aa

# linkedlist |0| ___ |1| ___ _____ |2|
# linkedlist |0| -> |1| -> |2| -> None

#linked list
class ListNode(object):
    def __init__(self, data, _next=None):
        self.data = data
        self.next = _next

    @staticmethod
    def walk(root):
        while root:
            yield root
            root = root.next

    @staticmethod
    def delete(root, data):
        """
        Deletes an element from list by the given `data`
        :param root:
        :param data:
        :return:
        """
        pass

    @staticmethod
    def rotate(root, number):
        """
        Returns new head of rotated linked list number of times `number`
        :param number:
        :return: root
        """
        pass

    @staticmethod
    def reverse(root):
        """
        Returns reversed new head of the list
        :param root:
        :return: new root
        """
        pass

    def __repr__(self):
        return str(self.data)


root = ListNode(0) # root.next = None
last = root
for i in xrange(1, 10):
    last.next = ListNode(i)
    last = last.next


list_n = list(ListNode.walk(root))

for i in list_n:
    if i.data == 3:
        list_n.remove(i)

r = [5,3,6,78,4,4,4,6,4,7,4]
for i in r:
    if i == 4:
        del r[i]
print r

print list_n
print list(ListNode.walk(root))