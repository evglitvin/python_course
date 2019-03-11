from collections import deque
import socket
from select import select
from concurrent.futures import ProcessPoolExecutor as Pool

def countdown(n):
    while n:
        yield n
        n -= 1


def fact(n):
    r = 1
    while n > 0:
        r *= n
        n -= 1
    return r


pool = Pool(10)
tasks = deque()
to_recv = {}
to_send = {}
to_future = {}


future_write_sock, future_read_sock = socket.socketpair()


def future_done(result):
    tasks.append(to_future.pop(result))
    future_write_sock.send('ok')


def future_notify():
    while True:
        yield 'recv', future_read_sock
        future_read_sock.recv(100)

tasks.append(future_notify())


def process(conn):
    while True:
        yield 'recv', conn
        data = conn.recv(100)  # blocking
        if not data:
            break
        # print "data ", data
        future = pool.submit(fact, int(data.strip()))
        yield 'future', future
        to_send = str(future.result()) # blocking
        # to_send = str(fact(int(data.strip()))) + '\n'
        yield 'send', conn
        conn.send(to_send)


def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('localhost', 8090))
    sock.listen(5)

    while True:
        yield 'recv', sock
        conn, addr = sock.accept()  # blocking
        print "accept"
        tasks.append(process(conn))
        # thread (process(conn))


tasks.append(server())


def run():
    while any([tasks, to_recv, to_send]):
        while not tasks:
            recvlist, sendlist, _ = select(to_recv, to_send , [])
            for s in sendlist:
                tasks.append(to_send.pop(s))
            for s in recvlist:
                tasks.append(to_recv.pop(s))

        task = tasks.popleft()

        try:
            reason, obj = next(task)
            if reason == 'recv':
                to_recv[obj] = task
            elif reason == 'send':
                to_send[obj] = task
            elif reason == 'future':
                to_future[obj] = task
                obj.add_done_callback(future_done)
        except (StopIteration, socket.error):
            pass


run()