import datetime
import random
import struct
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn, BaseRequestHandler
from _weakrefset import WeakSet

from pymongo import MongoClient


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
        return Point(self.x - other[0], self.y - other[1])

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])


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
        self.visible_pl = WeakSet() # ATTENTION! Cyclic links

    def get_field_of_view(self):
        return Point.validate_coord(self.pos - (16, 16)), Point.validate_coord(self.pos + (16, 16))

    def add_player(self, player):
        self.visible_pl.add(player)

    def add_players_nearby(self, player):
        player.add_player(self)
        self.add_player(player)

    def on_event(self, event):
        pass

    def notify_all(self, event):
        for pl in self.visible_pl:
            pl.on_event(event)

    def add_task(self, conn):
        conn.tasks.insert_one({'timeout':
                datetime.datetime.utcnow() + datetime.timedelta(seconds=random.randint(10, 601))})

    def __hash__(self):
        return self.id


class ThreadServer(ThreadingMixIn, HTTPServer):
    pass


class Handler(BaseHTTPRequestHandler):

    # def do_GET(self):


    def do_POST(self, ):
        # requests.get('http://localhost:8090/player/')
        print self.path    # /player/
        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')
        self.end_headers()

        # Send the html message
        self.wfile.write('Hello')
        return

# 643,25,436,7,53
# struct.pack('hhhh', 845,6,43,623)

# GET HTTP/1.0 /543634/432523

SERV = ('localhost', 8090)

if __name__ == '__main__':
    serv = ThreadServer(SERV, Handler)
    serv.serve_forever()