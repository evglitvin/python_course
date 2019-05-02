import sys


class SingletonMeta(type):
    __instances = {}

    def __new__(cls, *args, **kwargs):
        print(args)
        print(kwargs)

        what, bases, dict_types = args

        # changing bases whatever any is mentioned
        bases = (dict,)

        # adding attribute to class
        dict_types['get_zero'] = lambda x: 0

        return type(what, bases, dict_types)

    def __call__(cls, *args, **kwargs):
        inst = cls.__instances.get(cls)
        if not inst:
            cls.__instances[cls] = type.__call__(cls, *args, **kwargs)
            inst = cls.__instances[cls]
        return inst


class MyObject(list, metaclass=SingletonMeta):
    def __init__(self, a):
        super(MyObject, self).__init__()
        # print(self.__class__.mro())
        print("instance created")
        self.a = a

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


if __name__ == '__main__':
    print("Hello world")
    a = MyObject(11)
    print(a.get_a())
    a['gregre'] = 5436543
    print(a.get('gregre'))
    print("E mro: ", E.mro())

    print(a.get_zero())
    b = MyObject(12)
    print("next object", b.get_a())

    print(a.get_a())
    print(dir(sys.modules['__main__']))