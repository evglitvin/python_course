from collections import deque

from string import hexdigits, digits


def to_alphabet(n, s):
    if n == 0:
        return s[0]
    ret_val = deque()

    len_alpha = len(s)
    while n > 0:
        ret_val.appendleft(s[n % len_alpha])
        n /= len_alpha
    return "".join(ret_val)


def from_alphabet(s, alpha):
    ret = 0
    len_alpha = len(alpha)
    for idx, item in enumerate(s[::-1]):
        item = alpha.index(item)
        ret += item * len_alpha ** idx
    return ret

hexd = digits + 'abcdef'

print from_alphabet(to_alphabet(20, digits + 'abcdef'), hexd)
print to_alphabet(20, '01')
print to_alphabet(20, '01234567')
print from_alphabet('10100', '01')


