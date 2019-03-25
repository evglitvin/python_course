

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
    def rotate_left(root, number=1):
        """
        Returns new head of rotated linked list number of times `number`
        :param number: int number
        :return: root
        """
        head = root
        while number:
            new_head = head.next
            while root.next:
                root = root.next
            root.next = head
            head.next = None
            head = new_head
            number -= 1
        return head

    @staticmethod
    def reverse(root):
        """
        Returns reversed new head of the list
        :param root:
        :return: new root
        """
        # linkedlist |0| -> |1| -> |2| -> None
        # linkedlist |1| -> |0| -> |2| -> None
        # linkedlist |2| -> |1| -> |0|

        reversed_list = None
        while root:
            node = root
            root = node.next
            node.next = reversed_list
            reversed_list = node

        return reversed_list

    def __repr__(self):
        return str(self.data)


root = ListNode(0)  # root.next = None
last = root
for i in xrange(1, 10):
    last.next = ListNode(i)
    last = last.next
print list(ListNode.walk(root))
root = ListNode.rotate_left(root, 5)
print list(ListNode.walk(root))


# linkedlist |0| -> |1| -> |2| -> None
def swap(head):
    """
    Swaps two elements
    :param head: current head element
    :return: new head
    """
    if head and head.next:
        tmp = head.next
        head.next = tmp.next
        tmp.next = head
        return tmp
    return head


# prev = None
# tmp_node = root
# while tmp_node:
#     if tmp_node.data % 2:
#         if not prev:
#             tmp_node = swap(tmp_node)
#         else:
#             prev.next = swap(tmp_node)
#     prev = tmp_node
#     tmp_node = tmp_node.next
# print list(ListNode.walk(root))


# r = [5,3,6,78,4,4,4,6,4,7,4]
# for i in r:
#     if i == 4:
#         del r[i]
# print r
#
# print list_n
# print list(ListNode.walk(root))