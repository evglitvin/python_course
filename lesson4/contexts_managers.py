import io
import os
import pickle


class MyContext(object):
    def __init__(self, a):
        print "calling init"
        self.a = 1

    def __enter__(self):
        print "Entering context"
        self.a = 2
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print "Exit context"

        self.a = 3

    def get_a(self):
        return self.a


with MyContext(1) as c:
    print "Inside context"
    print c.get_a()


from contextlib import contextmanager


@contextmanager
def func_context(b):
    print "before context"
    yield b
    print "after context"


with func_context(5) as b:
    print "inside context", b



class A(object):
    def __init__(self, a):
        self.b = a
#
    def __getstate__(self):
        return 10

    def __setstate__(self, state):
        self.b = state

a = A(5)
with open("file1.blob", 'wb') as fr:
    pickle.dump(a, fr)


with open("file1.blob", 'rb') as fr:
    b = pickle.load(fr)

print b.b

l = bytes([5] * 40)

with open('bin_file.bin', 'wb') as bfile:
    bfile.write(l)

with open('bin_file.bin', 'rb') as bfile:
    print bfile.tell()
    bfile.seek(10, os.SEEK_CUR)
    print bfile.tell()
    print bfile.read(1)


class my_file(io.IOBase):
    def tell(self, *args, **kwargs):
        pass

    def seek(self, *args, **kwargs):
        pass

    def write(self, *args, **kwargs):
        pass