from collections import deque

l = [9,3,7,2,78,4,3,6,7,4]
"""
9 - 2
+
3 - 2
+
7 - 2
+
2
+
78 - 3
+...
"""
l = [9,3,7,2,78,4,3,6,7,4, 7 ,3, 4 , 5 , 6 , 7 ,8 ,9]

# l = []

def process_diff(in_list):
    res_sum = 0
    min_el = min(in_list)
    for idx in xrange(len(in_list) - 1):
        if in_list[idx] == min_el:
            min_el = min(in_list[idx + 1:])
            res_sum += in_list[idx]
        else:
            res_sum += (in_list[idx] - min_el)
    if min_el == in_list[-1]:
        res_sum += in_list[-1]
    return res_sum


def process_diff1(in_list):
    res_sum = 0
    min_el = min(in_list)
    counter = 0
    for idx in xrange(len(in_list) - 1):
        if in_list[idx] == min_el:
            res_sum -= min_el * (counter - 1)
            min_el = min(in_list[idx + 1:])
            counter = 0
        else:
            res_sum += in_list[idx]
            counter += 1
    if min_el == in_list[-1]:
        res_sum += in_list[-1]
    return res_sum

print process_diff(l),
print process_diff1(l)


def crypt(key, data):
    h = hash(key)
    lkey = len(key)
    res = []
    for i, ch in enumerate(data):
        res.append(chr(ord(ch) ^ ((h + ord(key[i % lkey])) & 0xff)))
    return "".join(res)

def decrypt(key, crypted_data):
    return crypt(key, crypted_data)

print decrypt('jfoerjfreio', crypt('jfoerjfreio', 'Hello')) == 'Hello'
print bin(ord('i')), bin(ord('j')), bin(ord('i') ^ ord('j'))