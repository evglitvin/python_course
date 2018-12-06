import os
from contextlib import contextmanager
from functools import wraps, partial
from io import IOBase
from struct import Struct
from time import time


class Enum(object):
    __values__ = None

    @classmethod
    def to_string(cls, key):
        try:
            return "{}.{}".format(cls.__name__, cls.__values__[key])
        except TypeError:
            try:
                n_dict = {item[1]: item[0] for item in cls.__dict__.iteritems()}
                cls.__values__ = n_dict
                return "{}.{}".format(cls.__name__, cls.__values__[key])
            except KeyError:
                return "UNKNOWN"
        except KeyError:
            return "UNKNOWN"


class JsonObject(object):
    def __init__(self, json_obj=None):
        self.__dict__.update(json_obj or {})

    __getattr__ = object.__dict__.get


class IndexedFile(object):
    INDEX_SIZE = 4

    BUCKET_LENGTH = 1000

    def __init__(self, filename):
        self._fname = filename

        try:
            self._size = os.stat(self._fname).st_size
        except OSError:
            self._size = 0

        name = os.path.splitext(filename)[0]
        self._idxfile = os.path.join(os.path.dirname(filename), name) + '.idx'
        try:
            self._file_obj = open(self._fname, 'r+a')
        except IOError:
            self._file_obj = open(self._fname, 'w+a')
        try:
            self._idxs_obj = open(self._idxfile, 'r+b')
        except IOError:
            self._idxs_obj = open(self._idxfile, 'w+b')
        self._idxs_data = self._idxs_obj.read()

        self._struct = Struct('>I')

        self._idxs = []
        self._idx_size = 0
        for idx in self.read_indexes():
            self._idxs.append(idx)
            self._idx_size += idx

        self.sum_idx_list = []

        self._offset = 0
        self._cline = 0

    def get_cached_sum(self, start, end):
        """
        Return cache sums
        :param start: int
        :param end: int
        :return: int
        """

        if start > 0:
            s = sum(self._idxs[start: end])
        else:
            try:
                s = self.sum_idx_list[end / self.BUCKET_LENGTH]
                s += sum(self._idxs[(end / self.BUCKET_LENGTH) * self.BUCKET_LENGTH: end])
            except IndexError:
                s = 0
                self.sum_idx_list = [0]
                i = 0
                while i < end / self.BUCKET_LENGTH:
                    temp_sum = sum(self._idxs[i * self.BUCKET_LENGTH: (i + 1) * self.BUCKET_LENGTH])
                    s += temp_sum
                    self.sum_idx_list.append(s)
                    i += 1
                # / - moving to start of the bucket
                s += sum(self._idxs[i * self.BUCKET_LENGTH: end])
        return s

    def read_indexes(self):
        for item_id in xrange(0, len(self._idxs_data), self.INDEX_SIZE):
            yield self._struct.unpack(self._idxs_data[item_id: item_id + self.INDEX_SIZE])[0]

    def writeline(self, line):
        assert self._idx_size == self._size, "Insert isn't allowed"
        self._file_obj.write(line + '\n')
        llen = len(line) + 1
        self._idxs.append(llen)
        self._idxs_obj.write(self._struct.pack(llen))
        self._size += llen
        self._idx_size += llen

    def readline(self):
        self._cline += 1
        return self._file_obj.readline()

    def seek(self, nline, whence=0):
        offset = 0
        if whence == 0:
            offset = self.get_cached_sum(0, nline)
            self._cline = nline
        elif whence == 1:
            assert nline > self._cline
            offset = sum(self._idxs[self._cline: nline + self._cline])
            self._cline += nline + self._cline
        elif whence == 2 and nline != 0:
            offset = -sum(self._idxs[nline:])
            self._cline = nline
        self._file_obj.seek(offset, whence)

    def close(self):
        if self._file_obj:
            self._file_obj.close()
            self._file_obj = None
        if self._idxs_obj:
            self._idxs_obj.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def print_duration(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        res = func(*args, **kwargs)
        print round(time() - start_time, 4)
        return res

    return wrapper