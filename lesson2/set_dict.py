

# set1 = set([[1]])    wrong set elements

set2 = {a for a in xrange(100) if a % 5}

tup = (1,) + (2, 3, 4)
for _ in xrange(10):
    tup += (10,)

s = []
for _ in xrange(10):
    s.append("jflerkgre")

s = ", ".join(s)


# dict
dict1 = {k: k**2 for k in xrange(100)}
print dict1

def get_spaces(s):
    return (i for i in s if i == ' ')

def get_repeeat_count(s, fn):
    d = {}
    for word in fn(s):
        d[word] = d.get(word, 0) + 1
    return d

# print get_repeeat_count('hfuwgbrek grnekgnre fhewklgnfew  fewjklfew  fewjfwe  fewjklfw', get_spaces)

from collections import defaultdict, OrderedDict

d = defaultdict(list)
d[7].append(1)
d[7].append(2)
print d


def get_dict(dict_fn):
    d = dict_fn()
    for i in xrange(-10, 10, 2):
        d[i] = i**2
    return d

print get_dict(OrderedDict).items()

print sorted(get_dict(dict).iteritems(), key=lambda x: x[1])


