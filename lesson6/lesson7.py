import random
import re

from python_course.lesson3.functions_and_classes import datetime
from python_course.lesson6.lesson6 import SingletonMeta


class Config(dict):
    """
    Parses parameters files like:
    PARAM1 = value
    Where value might be one of following types:
       int, str, datetime
    key: A-Za-z_0-9\-
    value: \w
    """
    __instances = {}

    _pattern = re.compile(r'\s*([A-Za-z_0-9\-]+)\s*=\s*([\w.]*)')

    def __getattr__(self, item):
        return self.get(item)

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
                self[match.group(1)] = self.decode(match.group(2))

    def _save_fn(self, fn):
        for k, v in self.iteritems():
            fn.write("{0} = {1}\n".format(k, str(v)))

    @staticmethod
    def process_fn(func_rw, f, mode='r'):
        if isinstance(f, basestring):
            with open(f, mode) as fn:
                func_rw(fn)
        else:
            fn = f
            func_rw(fn)

    def load(self, f):
        self.process_fn(self._load_fn, f)

    def save(self, f):
        self.process_fn(self._save_fn, f, mode='w')


def binary_search(sorted_list, item):

    """
    finds item in sorted list
    :param sorted_list: list
    :param item: int
    :return: None if no element found
    """
    start = 0
    end = len(sorted_list)
    while start < end:
        cur_item = (end + start) / 2
        if sorted_list[cur_item] > item:
            end = cur_item
        elif sorted_list[cur_item] < item:
            start = cur_item + 1
        elif sorted_list[cur_item] == item:
            return cur_item


def generate_sorted_stream(streams_count, number_of_elements):
    """
    :param streams_count:
    :param number_of_elements:
    :return:
    """
    return [sorted(random.randint(0, 100) for _ in xrange(number_of_elements))
            for _ in xrange(streams_count)]


def merge_lists(list_of_lists):
    """
    Merges lists into one sorted list
    :param list_of_lists:
    :return: sorted list
    """
    #     TODO implement sort logic

if __name__ == "__main__":
    # c1 = Config()
    # c2 = Config()
    #
    # l
    #
    # c1.load('file.cfg')
    # print c1['date'], type(c1['date'])
    # print c1.date, type(c1.date)

    sorted_list = [random.randint(0, 100) for _ in xrange(10)]
    # sorted_list = [8, 17, 21, 38, 43, 49, 49, 66, 70, 78]
    # sorted_list_with_item = [8, 17, 21, 38, 43, 49, 49, 50, 70, 78]
    print generate_sorted_stream(5, 3)