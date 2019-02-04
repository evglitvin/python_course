

# [00001001, 00000101, 00001000]
import random

tmp_list = list()
def get_uniq_numbers(numbers, length):
    global tmp_list
    for n in numbers:
        idx = n / 8
        bit_idx = n % 8
        if idx >= len(tmp_list):
            tmp_list += [0] * (idx - len(tmp_list) + 1)
        if tmp_list[idx] & (1 << bit_idx) == 0:
            tmp_list[idx] |= (1 << bit_idx)
            yield n


tmp_dict = {}
def get_uniq_numbers_d(numbers):
    # tmp_dict = {}
    for n in numbers:
        idx = n / 64
        bit_idx = n % 64
        el = tmp_dict.setdefault(idx, 0)
        if el & (1 << bit_idx) == 0:
            tmp_dict[idx] = el | (1 << bit_idx)
            yield n


# for i in get_uniq_numbers([0,4,2,5,3,6,3,6,3,3,100]):
#     print i
# print "*" * 40
# print len(tmp_list)
# print [bin(i) for i in  tmp_list]
yilded = set()
def generate_unique(input_array):
    # yilded = set()
    for i in input_array:
        if i not in yilded:
            yield i
            yilded.add(i)


def gen_random_int(n, number):
    for i in xrange(n):
        yield random.randint(0, number)


gen_numbers = list(gen_random_int(1000000, 1000000))
list(get_uniq_numbers_d(gen_numbers))
list(generate_unique(gen_numbers))

    # print i
print "*" * 40
print "bits", len(tmp_dict)
print "set", len(yilded)
# print [bin(i) for i in tmp_dict.itervalues()]