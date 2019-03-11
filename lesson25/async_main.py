## Based on Devid's Bizly code


from collections import deque
import socket
from select import select


def fact(n_str):
    n = int(n_str)
    r = 1
    while n > 0:
        r *= n
        n -= 1
    return r


class Loop(object):
    HOST_PORT = ('localhost', 8090)
    BACKLOG = 5

    tasks = deque()
    to_recv = {}
    to_send = {}

    processing_fn = None

    @classmethod
    def register(cls, fn):
        cls.processing_fn = staticmethod(fn)

    @classmethod
    def process(cls, conn):
        while True:
            yield 'recv', conn
            data = conn.recv(100)  # blocking
            if not data:
                break

            to_send = str(cls.processing_fn(data.strip())) + '\n'
            yield 'send', conn
            conn.send(to_send)

    @classmethod
    def server(cls):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(cls.HOST_PORT)
        sock.listen(cls.BACKLOG)

        while True:
            yield 'recv', sock
            conn, addr = sock.accept()  # blocking
            print "accept"
            cls.tasks.append(cls.process(conn))
            # thread (process(conn))

    @classmethod
    def run(cls):
        cls.tasks.append(cls.server())
        while any([cls.tasks, cls.to_recv, cls.to_send]):
            while not cls.tasks:
                recvlist, sendlist, _ = select(cls.to_recv, cls.to_send , [])
                for s in sendlist:
                    cls.tasks.append(cls.to_send.pop(s))
                for s in recvlist:
                    cls.tasks.append(cls.to_recv.pop(s))

            task = cls.tasks.popleft()

            try:
                reason, sock = next(task)
                if reason == 'recv':
                    cls.to_recv[sock] = task
                elif reason == 'send':
                    cls.to_send[sock] = task
            except (StopIteration, socket.error):
                pass


Loop.register(fact)
Loop.run()
