import json
import sys

d = {i: i**2 for i in xrange(10)}


class MyClass(object):
    def __init__(self):
        self.__attr = []
        self.__values = {}

    def __contains__(self, item):
        return True

    def __nonzero__(self):
        # expression
        return len(self.__attr) > 0 and len(self.__values) > 0

try:
    print d[5]
except KeyError:
    pass

c = MyClass()
if c:
    print "true"

l = [2,5,6,7,5,5,5]


def filter_n(iterable, filter_fn):
    idx = 0
    while idx < len(iterable):
        if filter_fn(iterable[idx]):
            del iterable[idx]
        else:
            idx += 1
    return iterable


l = filter_n(l, lambda x: not x % 5 and x % 10)
l = filter_n(l, lambda x: not x % 3)
print l

j = """{ 
       "name": "Jhon",
       "surname": "Smith",
       "age": 30,
       "links": [
            {"link1":5},
            {"link1":10, "link2":15},
            {"link1":5}
        ]
    }"""


class Attribute(dict):
    def __init__(self):
        self.a = 'Hello'

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            return None


a = Attribute()
a.update(json.loads(j))
# print a.name


def walk_json(json_data, prefix=None, key=None, indent=-1):
    if isinstance(json_data, list):
        for item in json_data:
            walk_json(item, indent=indent + 1)
    elif isinstance(json_data, dict):
        for k, v in json_data.iteritems():
            print (" " * indent * 4) + k + ": "
            walk_json(v, indent=indent + 1)
    else:
        ind = " " * indent * 4
        print ind + str(json_data)

print "#"*40
walk_json(json.loads(j))