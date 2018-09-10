
from __future__ import print_function
import socket
import threading
import time
from multiprocessing.dummy import Pool

lock = threading.RLock()


def process_conn(conn):
    lock.release()
    data = conn.recv(1024)
    if data:
        print('Recv: {0}'.format(data))
        conn.send('hello\r\n')


def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8000))
    sock.listen(2)

    timeout = time.time() + 300

    thr_pool = Pool(1000)

    while time.time() < timeout:
        conn, addr = sock.accept()
        # thr = Thread(target=process_conn, args=(conn,))
        # thr.start()
        thr_pool.apply_async(process_conn, args=(conn,))
    thr_pool.close()
    thr_pool.join()

    sock.close()


def run_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect(('localhost', 8000))

    sock.send('hello world\r\n')
    print(sock.recv(1024))
    sock.close()


import argparse

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--server', action='store_true')
    args = argparser.parse_args()
    if args.server:
        print("Server is running")
        run_server()
    else:
        print("Client started")
        run_client()
    print("DONE")
