class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def validate_coord(point):
        point.x = max(0, point.x)
        point.x = min(511, point.x)
        point.y = max(0, point.y)
        point.y = min(511, point.y)
        return point

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


class Map(object):
    def __init__(self):
        self.players = {} # k: idx of rectange (16 x 16)

    def add_player(self, player):
        x, y = player.pos.x, player.pos.y
        bucket = (x >> 5) | ((y >> 5) << 4)
        self.players.setdefault(bucket, set()).add(player)

    def get_players_around(self, player):
        top_left, bottom_right = player.get_field_of_view()
        bottom_left = Point(top_left.x, bottom_right.y)
        top_right = Point(bottom_right.x, top_left.y)
        set_b = {(p.x >> 5) | ((p.y >> 5) << 4) for p in [top_left, bottom_right, bottom_left, top_right]}
        for b in set_b:
            for pl in self.players.get(b, []):
                yield pl

    def get_visible_players(self, player):
        top_left, bottom_right = player.get_field_of_view()
        for pl in self.get_players_around(player):
            if (top_left.x < pl.pos.x < bottom_right.x and
                    top_left.y < pl.pos.y < bottom_right.y):
                yield pl


class Player(object):

    VIEW_SIZE = (32, 32)

    def __init__(self, id, pos=None):
        self.pos = pos
        self.id = id
        self.visible_pl = set() # ATTENTION! Cyclic links

    def get_field_of_view(self):
        return Point.validate_coord(self.pos - (16, 16)), Point.validate_coord(self.pos + (16, 16))

    def add_player(self, player):
        self.visible_pl.add(player)

    def add_players_nearby(self, player):
        player.add_player(self)
        self.add_player(player)

    def __hash__(self):
        return self.id


