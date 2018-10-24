import json
import select
import socket
import threading
import time
import weakref
from Queue import Empty, Queue


class Enum(object):
    __values__ = None

    @classmethod
    def to_string(cls, key):
        try:
            return "{}.{}".format(cls.__name__, cls.__values__[key])
        except TypeError:
            try:
                n_dict = {item[1]: item[0] for item in cls.__dict__.iteritems()}
                cls.__values__ = n_dict
                return "{}.{}".format(cls.__name__, cls.__values__[key])
            except KeyError:
                return "UNKNOWN"
        except KeyError:
            return "UNKNOWN"


class UserStatus(Enum):
    ONLINE = 1
    OFFLINE = 2
    BUSY = 3


class MessageType(Enum):
    INIT = 0
    STATUS = 1
    MESSAGE = 2
    ADD_FRIEND = 3
    DEL_FRIEND = 4


class DBUser(object):
    def __init__(self, u_id, nickname):
        self._u_id = hash(nickname)
        self._nickname = nickname
        self._status = UserStatus.OFFLINE
        # set of DBUser (friends)
        self._fr_users = weakref.WeakSet()

    def add_user(self, user):
        self._fr_users.add(user)

    def del_user(self, user):
        try:
            self._fr_users.remove(user)
        except KeyError:
            print "WARN: No such user for removing"

    def get_users(self):
        return self._fr_users

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, stat):
        self._status = stat

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, nick):
        self._nickname = nick

    def __hash__(self):
        return self._u_id


class DBUserDict(dict):
    pass


def process_connection(conn, connected_users, conn_map):
    data = conn.recv(1024)
    try:
        parsed_data = json.loads(data)
    except ValueError:
        db_user = conn_map.get(conn.fileno(), None)
        del conn_map[conn.fileno()]
        if db_user:
            db_user.status = UserStatus.OFFLINE
            print "user disconnected: {}".format(db_user.nickname)
            return False
    nick = parsed_data.get('nickname')
    if not nick:
        return True
    dbuser = connected_users.setdefault(nick, DBUser(None, nick))
    msg_type = parsed_data.get('type')
    if msg_type == MessageType.STATUS:
        # statuses = connected_users.get_statuses()
        statuses = [{"nickname": friend.nickname, "status": friend.status}
                    for friend in dbuser.get_users()]
        resp = {"nickname": nick,
                "friend": statuses}
        resp_json = json.dumps(resp)
        conn.send(resp_json)
    elif msg_type == MessageType.INIT:
        dbuser.status = parsed_data.get("status")
        conn_map[conn.fileno()] = dbuser
        print "{} connected status: {}".format(nick, UserStatus.to_string(dbuser.status))
    elif msg_type == MessageType.ADD_FRIEND:
        dbuser.status = parsed_data.get("status")
        print "{} connected status: {}".format(nick, UserStatus.to_string(dbuser.status))
    else:
        print "WARN: unknown message type"
    return True


class Driver(threading.Thread):
    def __init__(self, queue):
        super(Driver, self).__init__()
        self.daemon = True
        self._queue = queue
        self._connected_users = DBUserDict()
        self._connections = []
        self._conn_map = {}

    def run(self):
        while True:
            try:
                conn = self._queue.get(block=False)
                self._connections.append(conn)
            except Empty:
                pass
            # Windows failure
            if not self._connections:
                time.sleep(0.5)
                continue
            connects, _, _ = select.select(self._connections, [], [], 0.5)
            for conn in connects:
                if not process_connection(conn, self._connected_users, self._conn_map):
                    self._connections.remove(conn)

def run_server():
    q = Queue()

    next_user_id = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 8000))
    sock.listen(2)

    driver = Driver(q)
    driver.start()

    try:
        while True:
            conn, addr = sock.accept()
            # conn.recv(1024)
            # select.select()
            q.put(conn)

    except KeyboardInterrupt:
        print "Server is shutting down"


if __name__ == "__main__":
    run_server()

# def run_client():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#     sock.connect(('localhost', 8000))
#
#     sock.send('hello world\r\n')
#     print(sock.recv(1024))
#     sock.close()