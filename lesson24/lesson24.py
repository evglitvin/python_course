import SocketServer
import datetime
import profile
import random
import struct
import sys
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn, BaseRequestHandler
from _weakrefset import WeakSet
from collections import defaultdict

from pymongo import MongoClient


class Point(object):
    __slots__ = ('x', 'y')

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
        self.players = defaultdict(set) # k: idx of rectange (16 x 16)

    def add_player(self, player):
        x, y = player.pos.x, player.pos.y
        bucket = (x >> 5) | ((y >> 5) << 4)
        self.players[bucket].add(player)

    def get_players_around(self, top_left, bottom_right):
        bottom_left = Point(top_left.x, bottom_right.y)
        top_right = Point(bottom_right.x, top_left.y)
        set_b = {(p.x >> 5) | ((p.y >> 5) << 4) for p in [top_left, bottom_right, bottom_left, top_right]}
        for b in set_b:
            for pl in self.players.get(b, []):
                yield pl

    def get_visible_players(self, player):
        top_left, bottom_right = player.get_field_of_view()
        for pl in self.get_players_around(top_left, bottom_right):
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


class ThreadServer(ThreadingMixIn, SocketServer.TCPServer):
    pass


class GameController(object):
    def __init__(self):
        self._map = Map()
        self._init_players()

    def get_map(self):
        return self._map

    def _init_players(self):
        s_pl = set()
        while len(s_pl) < 20000:
            rand_pos = (random.randint(0, 512), random.randint(0, 512))
            while rand_pos in s_pl:
                rand_pos = (random.randint(0, 512), random.randint(0, 512))

            player = Player(len(s_pl), Point(*rand_pos))
            self._map.add_player(player)
            s_pl.add(rand_pos)
        print >> sys.stderr, "init completed"


class Handler(SocketServer.StreamRequestHandler):
    gc = GameController()

    def get_players(self):
        map = Handler.gc.get_map()
        tlx, tly, brx, bry = struct.unpack('hhhh', self.rfile.read(8))
        for pl in map.get_players_around(Point(tlx, tly), Point(brx, bry)):
            buf = struct.pack('ihh', pl.id, pl.pos.x, pl.pos.y)
            self.wfile.write(buf)

    def handle(self):
        self.get_players()
    # ROUTE = {'player/field_of_view': get_players}
    #
    # def do_POST(self):
    #     # requests.get('http://localhost:8090/player/')
    #        # /player/
    #     self.send_response(200)
    #     self.send_header('Content-type', 'application/octet-stream')
    #     self.end_headers()
    #
    #     self.ROUTE[self.path.strip('/')](self)
    #     # Send the html message
    #     # self.wfile.write('Hello')
    #     return



SERV = ('', 8090)


if __name__ == '__main__':
    serv = ThreadServer(SERV, Handler)
    serv.serve_forever()