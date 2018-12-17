import random
import time
import threading

a = 0
lock = threading.Lock()


# TODO implement data sharing between threads

class MThread(threading.Thread):
    def __init__(self):
        super(MThread, self).__init__()

    def run(self):
        global a
        for _ in xrange(1000):
            # lock.acquire()
            a += 1
            print self.name
            # lock.release()
            # time.sleep(random.random() * 0.1)


list_threads = []
for i in xrange(10):
    thr = MThread()
    thr.setName('name{}'.format(i))
    thr.setDaemon(True)
    thr.start()
    list_threads.append(thr)

for thr in list_threads:
    thr.join()
b = a + 1
# while threading.active_count() > 1:
#     # time.sleep(1)
#     print threading.active_count()

print 'shutting down a={}'.format(a)
