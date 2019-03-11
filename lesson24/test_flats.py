from random import random, randint
from matplotlib import pyplot
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple
Point = namedtuple("Point", ("x", "y"))


MAX_Y = 100


def gen_points(n):

    x, y = 0, randint(0, MAX_Y)

    count = 0
    while n:
        x += 1

        if count <= 0:
            if random() < 0.01:
                count = randint(100, 2000)
            y = randint(0, MAX_Y)
        else:
            count -= 1
        yield x, y
        n -= 1


def find_flats(points, max_val):

    start_x = 0
    counter = 0
    prev = None
    for idx, point in enumerate(points):
        if prev and prev[1] == point[1]:
            counter += 1
        else:
            if counter >= max_val:
                yield (start_x, idx), prev[1]  # prev
            counter = 0
            start_x = idx
        prev = point

    if counter >= max_val:
        yield (start_x, idx), prev[1]


list_points = list(gen_points(1000))
#
print list(find_flats(list_points, 100))



# Data for plotting


fig, ax = plt.subplots()
ax.plot([y for _, y in list_points])

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()

fig.savefig("test.png")
plt.show()



