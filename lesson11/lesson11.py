import re
from functools import wraps
from multiprocessing.dummy import Pool as ThreadPool
import requests
import time
from lesson18.threadpool import ThreadPool as Tp

LIST_RES = [
    'https://en.wikipedia.org/wiki/Money',
    'https://minfin.com.ua/currency/',
    'https://minfin.com.ua/currency/banks/kiev/',
    'https://loremipsum.io/ru/',
    'https://www.google.com/'
]

pattern = re.compile(r'<\s*{}\b'.format('p'))


def parse_url(url):
    result = requests.get(url)
    tags_count = 0
    for _ in pattern.finditer(result.text):
        tags_count += 1
    return tags_count


def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        stop = time.time() - start
        if hasattr(wrapper, 'performance'):
            wrapper.perfomance += stop
        else:
            wrapper.perfomance = stop
        return res
    return wrapper


@measure_time
def count_p_tags():

    tp = ThreadPool(10)
    for item in tp.imap_unordered(parse_url, LIST_RES):
        print item


@measure_time
def count_p_tags1():

    tp = Tp(10)
    for item in tp.imap_unordered(parse_url, LIST_RES):
        print item


@measure_time
def count_p_tags2():

    tp = Tp(10)
    for item in tp.map(parse_url, LIST_RES):
        print item


if __name__ == "__main__":
    count_p_tags()
    count_p_tags1()
    count_p_tags2()
    print count_p_tags.perfomance
    print count_p_tags1.perfomance
    print count_p_tags2.perfomance
