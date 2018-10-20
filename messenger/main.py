import json
import select
import socket
import weakref
from multiprocessing import Queue
from multiprocessing.pool import Pool


class UserStatus(object):
    ONLINE = 1
    OFFLINE = 2
    BUSY = 3


class DBUser(object):
    def __init__(self, u_id):
        self._u_id = u_id
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

    def __hash__(self):
        return hash(self._u_id)


class DBUserSet(set):
    pass


class DataContext(object):
    def __init__(self, queue):
        self.connected_users = DBUserSet()
        self._queue = queue

    def get_all_users(self):
        pass


def process_connection(conn, queue):
    data = conn.recv(1024)
    parsed_data = json.loads(data)
    print parsed_data['nickname'] + " connected"
    queue.put(parsed_data['nickname'])


def run_server():
    q = Queue()

    next_user_id = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8000))
    sock.listen(2)

    context = DataContext(q)

    pool = Pool(100)

    try:
        while True:
            conn, addr = sock.accept()
            # conn.recv(1024)
            # select.select()

            pool.apply_async(process_connection,
                             args=(conn, q))
    except KeyboardInterrupt:
        print "Server is shutting down"
    pool.close()
    pool.join()


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