import time
from Queue import Queue
import threading
from collections import deque
from random import randint


class Worker(threading.Thread):
    def __init__(self, func,  a_res, *args):
        super(Worker, self).__init__()
        self.setDaemon(True)
        self._func = func

        self._args = args
        self._async_res = a_res

    def run(self):
        self._async_res.set_started(True)
        self._async_res.set_result(self._func(*self._args))


class NotStartedError(Exception):
    pass


class AsyncResult(object):
    def __init__(self):
        # self._worker = worker
        self._result = None
        self._started = False
        self._ready = False

    def set_started(self, flag):
        self._started = flag

    def set_ready(self):
        self._ready = True

    def ready(self):
        return self._ready

    def set_result(self, result):
        self._result = result
        self.set_ready()

    def get(self):
        # if not self._started:
        while not self._started:
            time.sleep(0.005)

        while not self._ready:
            time.sleep(0.005)
        return self._result


class ThreadPool(object):
    def __init__(self, num_threads=8):
        self._num = num_threads
        # self._counter = 0
        # self._res_queue = Queue(1000)
        # self.results = {}

    def apply(self, func, *args):
        # TODO do limit of workers (use semaphore)
        async = AsyncResult()
        Worker(func, async, *args).start()
        return async


def func(*args):
    time.sleep(randint(2, 10))
    return sum(args)


# func = sum
pool = ThreadPool(10)


def gen_rand_numbers(numbers_len):
    for _ in xrange(numbers_len):
        yield randint(0, 100)


w2 = pool.apply(func, 1, 2, 3, 4)

apply_results = deque([])
for _ in xrange(10):
    r_numbers = tuple(gen_rand_numbers(randint(5, 10)))
    apply_results.append(pool.apply(func, *r_numbers))

start = time.time()
print "before waiting"


# for item in apply_results:
while apply_results:
    res = apply_results.popleft()
    if res.ready():
        print res.get()
    else:
        apply_results.append(res)

# print apply_results[0].get()
print "retrieved result {}".format(time.time() - start)