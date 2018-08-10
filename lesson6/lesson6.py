import sys

import re

from python_course.lesson3.functions_and_classes import datetime

sys.setrecursionlimit(2000)


def fact(n):
    if n == 0:
        return 1
    return fact(n - 1) * n


def fact_with_while(n):
    tmp_n = 1
    if n == 0:
        return 1
    while n > 1:
        tmp_n *= n
        n -= 1
    return tmp_n

print fact(5), fact_with_while(5)


class SingletonMeta(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if not cls.__instances.get(cls):
            cls.__instances[cls] = type.__call__(cls, *args, **kwargs)
        return cls.__instances.get(cls)


class Config(object):
    """
    Parses parameters files like:
    PARAM1 = value
    Where value might be one of following types:
       int, str, datetime
    key: A-Za-z_0-9\-
    value: \w
    """
    __metaclass__ = SingletonMeta

    _pattern = re.compile(r'\s*([A-Za-z_0-9\-]+)\s*=\s*([\w.]*)')

    def __init__(self):
        self.__params = {}

    @staticmethod
    def decode(value):
        try:
            return int(value)
        except ValueError:
            try:
                return datetime.from_time_str(value)
            except ValueError:
                return str(value)

    def _load_fn(self, fn):
        for line in fn:
            match = Config._pattern.match(line)
            if match:
                self.__params[match.group(1)] = self.decode(match.group(2))

    def _save_fn(self, fn):
        for k, v in self.__params.iteritems():
            fn.write("{0} = {1}\n".format(k, str(v)))

    @staticmethod
    def process_fn(func_rw, f):
        if isinstance(f, basestring):
            with open(f) as fn:
                func_rw(fn)
        else:
            fn = f
            func_rw(fn)

    def load(self, f):
        self.process_fn(self._load_fn, f)

    def save(self, f):
        self.process_fn(self._save_fn, f)

    def get_value(self, key):
        return self.__params.get(key)

    def set_value(self, key, value):
        self.__params[key] = value
# print dir(Config())

# print Config()._Config__params

if __name__ == "__main__":
    c1 = Config()
    c1.load('file.cfg')
    print c1.get_value('date'), type(c1.get_value('date'))