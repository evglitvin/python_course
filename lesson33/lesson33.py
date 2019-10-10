import time


def retry(waitobject, retry_exceptions):

    def wrapper(func):
        def decorator(*args, **kwargs):
            exc = None
            for _ in waitobject:
                try:
                    return func(*args, **kwargs)
                except retry_exceptions as e:
                    exc = e
            raise exc

        return decorator
    return wrapper


class Wait:
    def __init__(self, timeout):
        self._timeout = time.time() + timeout
        self._sleep_time = 1

    def __iter__(self):
        return self

    def __next__(self):
        if time.time() > self._timeout:
            raise StopIteration()
        time.sleep(self._sleep_time)


class ExponencialWait(Wait):
    def __next__(self):
        if time.time() > self._timeout:
            raise StopIteration()
        time.sleep(self._sleep_time)
        self._sleep_time *= 2


def wait(timeout):
    _sleep_time = 1
    _timeout = time.time() + timeout
    while time.time() < _timeout:
        yield
        time.sleep(_sleep_time)


def print_exception():
    """
    Prints variables when exception was raised
    :return: None
    """

    import sys

    def _print_locals(frame):
        print("Trace")
        local_p = frame.f_locals
        for item, value in local_p.items():
            print(" "*4, item, value)
        print()

    trace = sys.exc_info()[2]
    _print_locals(trace.tb_frame)

    tbnext = trace.tb_next
    while tbnext:
        _print_locals(tbnext.tb_frame)
        tbnext = tbnext.tb_next


def get_divizion():
    b = 1
    return b / 0


def get_div(a):
    return get_divizion()

try:
    get_div(45)
except Exception as e:
    print_exception()


@retry(ExponencialWait(10), (ZeroDivisionError, NameError))
def get_data():
    print("Calling get_data")
    d = a
    1 / 0

get_data()