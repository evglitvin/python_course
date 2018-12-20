import Queue
import random
import signal
import sys
import threading
import time


class MThreadWithShutdown(threading.Thread):

    def __init__(self, event, queue,  daemonize=True):
        super(MThreadWithShutdown, self).__init__()
        self.event = event
        self.setDaemon(daemonize)

    def run(self):
        while not self.event.is_set():
            a = random.random() * 10
            time.sleep(a)
            queue.put(a)
            print "{} is working".format(self.name)
        print "{} releases resources".format(self.name)


list_threads = []
event = threading.Event()

def term_all(a, b):
    print a
    event.set()

# SIGTERM for e.g. command kill from bash or os.kill() - equivalent
signal.signal(signal.SIGTERM, term_all)

# SIGTINT for Ctrl-C or stop from pycharm
signal.signal(signal.SIGINT, term_all)

queue = Queue.Queue(1000)

for i in xrange(10):
    # thr = MThread(sem) or ...

    thr = MThreadWithShutdown(event, queue)
    thr.setName('name{}'.format(i))
    thr.start()
    list_threads.append(thr)

timeout = time.time() + 30
sum_times = 0
while not event.is_set() and timeout > time.time():
    time.sleep(2)
    try:
        sum_times += queue.get(False)
    except Queue.Empty:
        pass
    print "main is still alive"

event.set()

for thr in list_threads:
    thr.join()

while not queue.empty():
    try:
        sum_times += queue.get(False)
    except Queue.Empty:
        print sys.exc_traceback

# while threading.active_count() > 1:
#     # time.sleep(1)
#     print threading.active_count()
print "sum = {}".format(sum_times)

print 'shutting down main thread'