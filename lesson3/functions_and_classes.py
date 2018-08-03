from __future__ import print_function

class A(object):
    @classmethod
    def get_inst(cls, a):
        print("cls = ", cls)
        return getattr(cls, "__init__")

    @staticmethod
    def get_static_calculation():
        return 1

    def get_attr(self):
        return 1

    def jump(self):
        print("can't jumped")


class B(A):
    pass


print(A.get_inst(1))
print(A.get_static_calculation())
print(A.get_attr(A()), A().get_attr())

print(B().jump())


print("=" * 30)


import time

class datetime(object):
    __slots__ = ("_day", "_month", "_year", "_hour", "_mins", "_sec")
    """
    Represents date and time object with additional methods
    """

    def __init__(self, day=None, month=None, year=None, hour=None, mins=None, sec=None):
        """
        :param day: int day
        :param month: int month
        :param year: int year
        :param hour: int hour
        :param mins: int mins
        :param sec: int sec
        """
        dt = time.localtime()

        self._day = day or dt.tm_mday
        self._month = month or dt.tm_mon
        self._year = year or dt.tm_year
        self._hour = hour or dt.tm_hour
        self._mins = mins or dt.tm_min
        self._sec = sec or dt.tm_sec

    def __repr__(self):
        """
        :return: str string representation of the object
        """
        return "{}".format({k: getattr(self, k) for k in self.__slots__})

    def __str__(self):
        """
        :return: str string in format "D.M.Y h:m:s"
        """
        return "{0[_day]:02}.{0[_month]:02}.{0[_year]} {0[_hour]}:{0[_mins]}:{0[_sec]}".format(
            {k: getattr(self, k) for k in self.__slots__})

    def is_day(self):
        """
        Returns True if now is a day
        :return: bool: True if its day, False - otherwise
        """
        return 4 < self._hour < 20

    @classmethod
    def from_time_str(cls, str_time):
        """
        Helper method to transform string to datetime
        :param str_time:
        :return:
        """
        # TODO need to be extended by time as well
        d, m, y = str_time.split(".")
        return cls(int(d), int(m), int(y))

    @staticmethod
    def is_leap_year(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def __sub__(self, other):
        """
        Return number of seconds from other datetime
        :param other: datetime object
        :return: int: number of seconds
        """
        # TODO implement it
        # raise NotImplementedError
        pass

print(datetime(month=5))
print(str(datetime(month=5)))
print(datetime.from_time_str("2.07.2018").is_day())

d = datetime.from_time_str("2.07.2018")
d._hour = 21
print(d.is_day())

print(datetime.is_leap_year(2100))


class my_datetime(datetime):
    @classmethod
    def from_time_str(cls, str_time):
        return super(my_datetime, cls).from_time_str(str_time)

print(my_datetime.from_time_str("01.01.2019") - my_datetime())

pow_by_2 = lambda x, t: x ** 2 + t

print(list(pow_by_2(x, 5) for x in xrange(10,100,3)))


def func(x, n):
    print("x=", x)
    return x * 3 + n

func(6, 3)
func(6, 3)
func(30, 3)
func(20, 3)
func(30, 3)
func(100, 3)


from functools import partial
new_func = partial(func, n=3)
print("=" * 80)
print(new_func(30))
print(new_func(100))

