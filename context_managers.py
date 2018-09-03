class ManagedFile(object):
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.file = open(self.name, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()


from contextlib import contextmanager


@contextmanager
def managed_file(name):
    try:
        f = open(name, 'w')
        yield f
    finally:
        f.close()


class Indenter(object):
    def __init__(self):
        self.level = 0

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.level -= 1

    def print_ind(self, text):
        print ' ' * self.level + text


with Indenter() as indent:
    indent.print_ind('Hi')
    with indent:
        indent.print_ind('Hello')
        with indent:
            indent.print_ind('Bonjour')
    indent.print_ind('Hello')


class Test(object):
    def __init__(self):
        self.foo = 11
        self._bar = 23
        self.__baz = 42


class ExtendedTest(Test):
    def __init__(self):
        super().__init__()
        self.foo = 'overridden'
        self._bar = 'overridden'
        self.__baz = 'overridden'


t = Test()

for i in dir(t):
    print i