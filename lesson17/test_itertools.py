
#  monkey patching
class my_itertools(object):
    def __getattribute__(self, item):
        import itertools
        print item.center(30, '*')
        return getattr(itertools, item)

    # def __getattribute__(self, item):
    #     import itertools
    #     return getattr(itertools, item)

itertools = my_itertools()


# group by repeated value in iter
s = 'kl;;;;feewkgl;'

for k, item in itertools.groupby(s):
    print k, list(item)

s = '12345678'
print zip(s, xrange(len(s)-2))

for item in itertools.izip(s, xrange(len(s)-2)):
    print item

for item in itertools.izip_longest(s, xrange(len(s) - 2), fillvalue=None):
    print item

for item in itertools.permutations('abc', 2):
    print item


def cycle(iterable):
    c_iter = iter(iterable)
    while True:
        try:
            yield c_iter.next()
        except StopIteration:
            c_iter = iter(iterable)
            yield c_iter.next()

# itertools.cycle = cycle

c = itertools.cycle('abc')
for i in xrange(10):
    print next(c)
