def lru_cache(func):
    """
    :return: wrapped func
    """
    __cache = {}

    def wrapper(*args, **kwargs):
        try:
            return __cache[args]
        except KeyError:
            __cache[args] = func(*args, **kwargs)
            return __cache[args]
    return wrapper


def func(n):
    print "I've got {}".format(n)
    return n - 1

func = lru_cache(func)

# for _ in xrange(5):
#     # function will be called only once as argument is the same
#     print func(100)


