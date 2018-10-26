import json
import select
import socket
import threading
import time
from Queue import Empty, Queue

from messenger.dbuser import DBUser
from messenger.message import Message, MessageProcessor
from messenger.utils import Enum


class UserStatus(Enum):
    ONLINE = 1
    OFFLINE = 2
    BUSY = 3


def process_connection(conn, msg_proc, conn_map):
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

    message = Message.parse(parsed_data)
    if message:
        msg_proc.process_message(message)
    return True


class Driver(threading.Thread):
    def __init__(self, queue):
        super(Driver, self).__init__()
        self.daemon = True
        self._queue = queue
        self._connections = []
        self._conn_map = {}
        self._msg_processor = MessageProcessor()

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
                if not process_connection(conn, self._msg_processor, self._conn_map):
                    self._connections.remove(conn)


def run_server():
    q = Queue()

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
