import random
import string
from collections import deque



class Iterator(object):
    def __init__(self, iterable):
        self._idx = 0
        self._iter = iterable

    def __iter__(self):

        while True:
            yield self._iter[self._idx % len(self._iter)]
            self._idx += 1

    def next(self):
        if self._idx >= len(self._iter):
            raise StopIteration
        res = self._iter[self._idx]
        self._idx += 1
        return res

# # print Iterator
# for i in Iterator([2,3,4]):
#     print i
#
# it = iter(Iterator([4,8,3,7]))
# print next(it)
# print it.next()
# print it.next()
# print it.next()
# print it.next()
# print it.next()


l1 = [[2, 5, 8], [1, 5, 6], [1, 7, 9, 10, 80]]


def merge(iterable):
    iterators = [iter(item) for item in iterable]
    stack_elements = []

    for it in iterators:
        try:
            stack_elements.append((it.next(), it))
        except StopIteration:
            pass
    print "step1", stack_elements
    while stack_elements:
        minvalue = None
        min_idx = None
        for idx, item in enumerate(stack_elements):
            value, it = item
            if minvalue is None or minvalue > value:
                min_idx = idx
                minvalue = value

        minitem = stack_elements.pop(min_idx)
        try:
            yield minitem[0]
            stack_elements.append((minitem[1].next(), minitem[1]))
        except StopIteration:
            pass


print list(merge(l1))

SYMBOLS = string.ascii_lowercase


def gen_random_char(n):
    # generate symbols
    random.seed(n)
    while True:
        yield random.choice(SYMBOLS)


def find(iterable, word):
    counter = 0
    match = 0
    l_word = len(word)
    for char in iterable:
        if char == word[match]:
            match += 1
        else:
            match = 0
            if char == word[match]:
                match += 1
        counter += 1

        if match == l_word:
            return counter - l_word

    return -1


assert find('cacat', 'cat') == 2

print find(gen_random_char(1), 'cat')

