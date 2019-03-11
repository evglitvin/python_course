import socket
import time
from threading import Thread

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('', 8090))

n = 0


def monitor():
    global n
    while True:
        print n
        n = 0
        time.sleep(1)


t = Thread(target=monitor)
t.setDaemon(True)
t.start()

while True:
    sock.send(str(0))
    int(sock.recv(100))
    n += 1
