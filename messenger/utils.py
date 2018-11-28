import os
from io import IOBase
from struct import Struct


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

        self._offset = 0
        self._cline = 0

    def read_indexes(self):
        for item_id in xrange(0, len(self._idxs_data), self.INDEX_SIZE):
            yield self._struct.unpack(self._idxs_data[item_id: item_id + self.INDEX_SIZE])[0]

    def writeline(self, line):
        assert self._offset == self._size, "Insert isn't allowed"
        self._file_obj.write(line + '\n')
        self._idxs.append(len(line) + 1)
        self._idxs_obj.write(self._struct.pack(len(line) + 1))
        self._size += len(line) + 1

    def readline(self, limit):
        return self._file_obj.readline(limit)

    def seek(self, nline, whence=0):
        offset = 0
        if whence == 0:
            offset = sum(self._idxs[0: nline])
        elif whence == 1:
            offset = sum(self._idxs[self._cline: nline])
        elif whence == 2 and nline != 0:
            offset = -sum(self._idxs[-nline:])
        self._cline = nline
        self._file_obj.seek(offset, whence)

    def close(self):
        if self._file_obj:
            self._file_obj.close()
            self._file_obj = None
        if self._idxs_obj:
            self._idxs_obj.close()


ifile = IndexedFile('name1.txt')
ifile.seek(0, 2)
ifile.writeline('hello')
ifile.close()
