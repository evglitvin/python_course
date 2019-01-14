import time
from collections import deque
from random import randint

# map(f, [])


from multiprocessing import Pool
# imap_unordered


def max_power(l):
    time.sleep(randint(10))
    return [i ** 5 for i in l]
# multiprocessing

pool = Pool(10)
# pool.
# res = pool.map(max_power, (randint(0, 100) for _ in xrange(10)))

# for item in pool.imap_unordered(max_power, (randint(0, 100) for _ in xrange(10))):
#     print item

# future_res = pool.apply_async(max_power, (randint(0, 100) for _ in xrange(10)))
apply_results = deque([])
for _ in xrange(10):
    apply_results.append(pool.apply_async(max_power, ([randint(0, 100) for i in xrange(randint(1,5))],)))

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


# print res
