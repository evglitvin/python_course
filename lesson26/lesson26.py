from functools import wraps

count = 0


class MyObject(object):
    def __init__(self):
        global count
        self._id = count
        print "created ", count
        count += 1


def decorator(fn):

    obj = MyObject()

    @wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(obj)
    return wrapper


def func(obj):
    return obj._id

func = decorator(func)

@decorator
def func1(obj):
    return obj._id


print func(1)
print func1(2)


def get_min(self, a, b):
    return min(a,b)

class MyClass(object):
    method = classmethod(get_min)
    count = 0

print MyClass.count
print MyClass.method(3,5)