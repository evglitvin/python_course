def get_days_count(year):
    assert isinstance(year, int)
    return 366 if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else 365


def feb_days(year):
    return 28 if get_days_count(year) == 365 else 29


def days_to_new_year(current_year, month, day):
    feb = feb_days(current_year)
    days_in_month = (31, feb, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    counter = 0
    for i in xrange(month - 1, len(days_in_month), 1):
        counter += days_in_month[i]
    counter -= day
    return counter


print days_to_new_year(2018, 8, 3)

assert get_days_count(2000) == 366
assert get_days_count(2018) == 365
assert get_days_count(2100) == 365
