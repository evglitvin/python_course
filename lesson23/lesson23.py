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
l = [1, 3, 3, 2, 5]
# l = [5, 1, 3, 4, 6, 2]
# l = []

def finalPrice(prices):
    # Write your code here

    res_sum = 0
    min_el = min(prices)
    idxs = []
    for idx in xrange(len(prices) - 1):
        if prices[idx] == min_el:
            min_el = min(prices[idx + 1:])
            idxs.append(idx)
            res_sum += prices[idx]
        else:
            res_sum += (prices[idx] - min_el)
    if min_el <= prices[-1]:
        res_sum += prices[-1]
        idxs.append(len(prices) - 1)
    print res_sum
    print " ".join(str(i) for i in idxs)

finalPrice(l)








def process_diff(in_list):
    res_sum = 0
    min_el = min(in_list)
    idxs = []
    for idx in xrange(len(in_list) - 1):
        if in_list[idx] == min_el:
            min_el = min(in_list[idx + 1:])
            idxs.append(idx)
            res_sum += in_list[idx]
        else:
            res_sum += (in_list[idx] - min_el)
    if min_el == in_list[-1]:
        res_sum += in_list[-1]
        idxs.append(len(in_list) - 1)
    print res_sum
    print " ".join(str(i) for i in idxs)


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
# print process_diff1(l)


def crypt(key, data):
    h = hash(key)
    lkey = len(key)
    res = []
    for i, ch in enumerate(data):
        res.append(chr(ord(ch) ^ ((h + ord(key[i % lkey])) & 0xff)))
    return "".join(res)


def decrypt(key, crypted_data):
    return crypt(key, crypted_data)


secret_key = 'jfoerjfreio'
print decrypt(secret_key, crypt(secret_key, 'Hello')) == 'Hello'

# we shouldn't find the secret using in_data and crypted data
assert decrypt(crypt(secret_key, 'Hello'), 'Hello') != secret_key
