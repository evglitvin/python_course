
class SingletonMeta(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        inst = cls.__instances.get(cls)
        if not inst:
            cls.__instances[cls] = type.__call__(cls, *args, **kwargs)
            inst = cls.__instances[cls]
        return inst


class MyObject(object):
    __metaclass__ = SingletonMeta
    # _instances = {}

    def __init__(self, a):
        super(MyObject, self).__init__()
        # print(self.__class__.mro())
        print("instance created")
        self.a = a

    # def __new__(cls, *args, **kwargs):
    #     print(cls, args, kwargs)
    #     inst = cls._instances.get(cls)
    #     if not inst:
    #         cls._instances[cls] = object.__new__(cls, *args, **kwargs)
    #         inst = cls._instances[cls]
    #     else:
    #         cls.__init__ = object.__init__
    #     return inst

    def get_a(self):
        return self.a

    def __getattr__(self, item):
        return self.__dict__.get(item)

    __setitem__ = dict.__setitem__


if __name__ == '__main__':

    a = MyObject(11)
    b = MyObject(12)
    assert id(a) == id(b)
    print(b.get_a())
    print(a.get_a())