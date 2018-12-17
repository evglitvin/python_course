import time
from multiprocessing import Process


def func():
    start = time.time()
    a = 0
    for _ in xrange(1000000):
        a += 1
    print time.time() - start


list_pr = []
start_p = time.time()
for _ in xrange(6):
    pr = Process(target=func)
    pr.start()
    list_pr.append(pr)

for pr in list_pr:
    pr.join()
print 'multipr {}'.format(time.time() - start_p)

start = time.time()
b = 0
for _ in xrange(1000000 * 6):
    b += 1
print "Single {}".format(time.time() - start)