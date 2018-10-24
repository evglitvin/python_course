import json
import socket
from argparse import ArgumentParser

from messenger.main import MessageType, UserStatus


def run_client():
    parser = ArgumentParser('Client for messenger')
    parser.add_argument('--nickname', required=True)
    parser.add_argument('--status', type=int, required=True)
    args = parser.parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect(('localhost', 8000))

    msg = {"nickname": args.nickname,
           "type": MessageType.INIT,
           "status": args.status}
    sock.send(json.dumps(msg))
    print(sock.recv(1024))
    sock.close()


if __name__ == "__main__":
    run_client()
