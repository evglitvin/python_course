def test_func(a):
    # use a for reading
    f = a

    # creating new var
    if expr:
        a = 1

    try:
        open('fjireogfe')
        g = 5
    except IOError as e:
        pass

    if expr:
        g = 1
    else:
        g = 1
    print g


set_1 = {0, 128, 1, 3, 256}
for item in set_1:
    print item


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])


class Rect(object):
    def __init__(self, (x, y)=(0, 0), (width, height)=(100, 100)):
        self._pos = Point(x, y)
        self._size = width, height

    @property
    def pos(self):
        return self._pos

    @property
    def size(self):
        return self._size

    @property
    def center(self):
        return (self._pos.x + self._size[0]) / 2, (self._pos.y + self._size[1]) / 2

    @property
    def bounding_box(self):
        return self._pos, self._pos + self._size, \
               self._pos + (self._pos.x, self._size[1]), \
               self._pos + (self._size[0], self._pos.y)

    def point_in_rect(self, point):
        return self._pos.x < point.x and self._pos.y < point.y and \
               self._pos.x + self._size[0] > point.x and self._pos.y + self._size[1] > point.y

    __contains__ = point_in_rect

    def overlap(self, other):
        for point in other.bounding_box:
            if self.point_in_rect(point):
                return True
        for point in self.bounding_box:
            if other.point_in_rect(point):
                return True

        return False


print Rect((0, 0), (200, 200)).overlap(Rect((200, 200), (300, 300)))