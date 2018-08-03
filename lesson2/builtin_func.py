

b = [False] * 10
b[3] = 7
print all(b), any(b)

b = [True] * 10
print all(b), any(b)

a = bool(0)


def func():
    return 1

class PseudoFunc(object):
    def __init__(self, a):
        self._a = a

    # def __cmp__(self, other):
    #     return self._a - other._a

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, v):
        self._a = v

    def __call__(self, *args, **kwargs):
       return 1

c = PseudoFunc(1)
c()
print "Callable ", callable(c), callable(a), callable(PseudoFunc)

c1 = PseudoFunc(2)
print sorted([c1, c])[0]._a

l = xrange(-10, 10, 2)
print list(l)
print "filter", filter(None, l)
print filter(lambda x: x % 4, l)

print "float: {0[name]}".format(dict(name=1))

print id(c) == id(c1)

print map(lambda x: x**2, l)
#  better to use listcomprehension instead where its possible
print (i ** 2 for i in l)

print max(c1, c)._a

with open('/tmp/filenaame', 'w') as f:
    f.write('0')

print reduce(lambda a, b: (a, b), l)

class A(object):
    def __getattr__(self,item):
        return True
a = A()
setattr(a, "name", "huiname")
# a.name = 'name'
print dir(a), a.name

