import math


def get_bits_count(n):
    count = 0
    while n:
        if n & 1:
            count += 1
        n = n >> 1
    return count


def get_bits_count1(n):
    count = 0
    while n:
        n = n & (n - 1)
        count += 1
    return count


def get_bits_for_number(n):
    return int(math.ceil(math.log(n, 2)))


def get_cipher_for_number(n):
    return int(math.ceil(math.log(n, 10)))


# print get_bits_for_number(758935)  # number of bits needed to save the number
# print get_cipher_for_number(758935)  # number of ciphers needed to save the number
