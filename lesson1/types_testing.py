
# default arguments
import math

ttt = 0

def func(l=[]): # wrong: default value is mutable
    global ttt

    for temp_var in xrange(10):
        pass

    print temp_var == 9
    ttt = 5
    in_list = l or []
    in_list.append(1)
    return in_list

l = [1, 2, 4, 4, 6, 7]
# b = l[2:6]   # copy of l
l[2:5] = [0]
print "test l", l


s = {i for i in xrange(10)} == set(xrange(10))
s1 = {i for i in xrange(2, 10, 2)}
print s & s1
print s | s1
print s - s1
print s ^ s1


b = l
print l, b
idx = 0
idx_del = -1
while idx < len(b):
    if b[idx] % 2 == 0:
        del b[idx]
        idx_del = idx
    else:
        idx += 1
if idx_del == -1:
    print idx_del
print b

# list-comprehentions
l = (item for item in read_lines if my_filter(x))


def my_filter(x):
    return math.floor(x) != 0

f = filter(my_filter, [0.5435, 2.4325,  5.43242, 43.252])

l1 = xrange(10 ** 10)

# too large list
# useless compre

print l1


def my_xrange(start=None, stop=None, step=1):
    n = stop
    x0 = 0
    if not stop:
        n = start
    else:
        x0 = start

    while x0 < n:
        yield x0
        x0 += step

from operator import *

def my_range(start=None, stop=None, step=1):
    lt_fn = lt
    and_(lt(start, stop), gt(step, 0))
    and_(lt(start, stop), gt(step, 0))
    if (start < stop and step > 0) or (start > stop and step < 0):
        raise ValueError("step should go from start to end")
    n = stop
    x0 = 0
    if not stop:
        n = start
    else:
        x0 = start
    ret_list = []
    while x0 < n:
        ret_list.append(x0)
        x0 += step
    return ret_list


my_gen = my_xrange(5)
print my_gen
for i in my_xrange(5):
    print i


assert list(my_xrange(10)) == list(xrange(10))
assert list(my_xrange(10, 20)) == list(xrange(10, 20))
assert list(my_xrange(10, 20, 2)) == list(xrange(10, 20, 2))