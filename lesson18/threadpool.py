import time
from Queue import Queue, Empty
import threading
from collections import deque


class Worker(threading.Thread):
    def __init__(self, task_queue):
        super(Worker, self).__init__()
        self._task_queue = task_queue

        self.setDaemon(True)

    def run(self):
        # Queue.empty()
        while True:
            try:
                a_res, sem, func, args = self._task_queue.get()
            except Empty:
                break
            sem.acquire()
            a_res.set_started(True)
            a_res.set_result(func(*args))
            sem.release()


class SmartSemaphore(threading._Semaphore):
    # Using semaphore to get the value
    def get_value(self):
        return self._Semaphore__value


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
        self._task_queue = Queue()
        self._sem = SmartSemaphore(num_threads)

    def apply(self, func, *args):
        async = AsyncResult()
        self._task_queue.put((async, self._sem, func, args))
        if self._sem.get_value() > 0:
            Worker(self._task_queue).start()
        return async

    def imap_unordered(self, func, iter_args):
        apply_results = deque(self.apply(func, arg) for arg in iter_args)

        while apply_results:
            res = apply_results.popleft()
            if res.ready():
                yield res.get()
            else:
                apply_results.append(res)
                time.sleep(0.005)

    def map(self, func, iter_args):
        apply_results = [self.apply(func, arg) for arg in iter_args]
        return map(AsyncResult.get, apply_results)

    def get_num_workers(self):
        return self._num - self._sem.get_value()

    # see lesson11 with tests