import os


class Reader(object):
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        print "read from this {}".format(self.__class__.__name__)

    def set_filename(self, filename):
        self.filename = filename
        return self

    def set_chunk_size(self, size):
        self.size = size
        return self


class TextReader(Reader):
    pass
    # def read(self):
    #     #TODO reading from text
    #     print "read from this {}".format(self.__class__.__name__)
    #

class BinaryReader(Reader):
    pass


def fab_method(filename):
    _, ext = os.path.splitext(filename)
    if ext == '.bin':
        return BinaryReader
    elif ext == '.txt':
        return TextReader


reader = fab_method('name.bin')
read_instance = reader('name.bin')
read_instance.read()


class Singleton(type):
    instances = {}

    # TODO implement singleton
    def __call__(self, *args, **kwargs):
        return self


class Config(object):
    __metaclass__ = Singleton

    def __init__(self, a):
        self.a = a
        print "Initialized config"


singleton = Config(2) # instance of Singleton will be returned
singleton1 = Config(5)

print singleton, singleton1