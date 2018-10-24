import json
import socket

from messenger.main import MessageType


def run_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect(('localhost', 8000))

    msg = {"nickname": "Eugene", "type": MessageType.INIT}
    sock.send(json.dumps(msg))
    print(sock.recv(1024))
    sock.close()


if __name__ == "__main__":
    run_client()
