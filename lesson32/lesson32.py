import sys
from importlib import reload


class SingletonMeta(type):
    _instances = {}

    # def __new__(cls, *args, **kwargs):
    #     print(args)
    #     print(kwargs)
    #
    #     what, bases, dict_types = args
    #
    #     # changing bases whatever any is mentioned
    #     bases = (dict,)
    #
    #     # adding attribute to class
    #     dict_types['get_zero'] = lambda x: 0
    #
    #     return type(what, bases, dict_types)

    def __call__(cls, *args, **kwargs):
        inst = cls._instances.get(cls)
        if inst is None:
            inst = type.__call__(cls, *args, **kwargs)
            cls._instances[cls] = inst
        return inst


class MyObject(list,  metaclass=SingletonMeta):
    def __init__(self, a):
        super(MyObject, self).__init__()
        # print(self.__class__.mro())
        print("instance created")
        self.a = a

    def get_a(self):
        return self.a

    def __getattr__(self, item):
        return self.__dict__.get(item)

    __setitem__ = dict.__setitem__


def get_a(x):
    return x.a


MyObject.get_a = get_a


class A(object):
    pass


class B(A):
    pass


class C(A):
    pass


class D(B):
    pass


class E(D, dict):
    pass


if __name__ == __name__:
    print("E mro: ", E.mro())

    a = MyObject(11)
    b = MyObject(12)
    print(b.get_a())
    print(a.get_a())
    print(dir(sys.modules['__main__']))
    # reload()