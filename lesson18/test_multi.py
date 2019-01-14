import threading

a = 0
#
sem = threading.BoundedSemaphore(10)

# TODO implement data sharing between threads


class MThread(threading.Thread):

    def __init__(self, lock, daemonize=True):
        super(MThread, self).__init__()
        self.lock = lock
        self.setDaemon(daemonize)

    def run(self):
        global a
        for _ in xrange(1000):
            self.lock.acquire()

            a = a + 1
            print self.name

            self.lock.release()

            kfel;skfe;
            # time.sleep(random.random() * 0.1)


list_threads = []
sem = threading.Semaphore(10)
lock = threading.RLock()
for i in xrange(1000):
    # thr = MThread(sem) or ...

    thr = MThread(sem)
    thr.setName('name{}'.format(i))
    thr.start()
    list_threads.append(thr)

for thr in list_threads:
    thr.join()
b = a + 1
# while threading.active_count() > 1:
#     # time.sleep(1)
#     print threading.active_count()

print 'shutting down a={}'.format(a)

