import json
import socket
import time
from argparse import ArgumentParser
from messenger.message import MessageType, Message
from messenger.user_status import UserStatus


def _create_message(nickname,
                    m_type=MessageType.UNKNOWN_TYPE,
                    **kwargs):
    m = Message()
    m.type = m_type
    m.nickname = nickname
    m.update(kwargs)
    return m


def wait(message):
    time.sleep(10)

def add_friend(message):
    pass

PROCESS_MAP_FN = {
    'wait': wait,
    'add_friend': add_friend,
}

def run_client():
    parser = ArgumentParser('Client for messenger')
    parser.add_argument('--nickname', required=True)
    parser.add_argument('--status', type=int, required=True)
    parser.add_argument('--wait', action='store_true')
    parser.add_argument('--message', default='')
    parser.add_argument('--add-friend', action='store_true')

    args = parser.parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect(('localhost', 8000))
    msg = {"nickname": args.nickname,
           "type": MessageType.INIT,
           "status": args.status}
    sock.send(json.dumps(msg))
    # Make non-blocking
    print(sock.recv(1024))
    print "Connected"
    m = _create_message(args.nickname, status=args.status)

    if args.wait:
        PROCESS_MAP_FN['wait'](m)

    if args.send_message:
        m.type = MessageType.MESSAGE
        m.message = dict(sender=args.nickname,
                         content=args.send_message)
        sock.send(m.to_json())
        sock.recv()

    sock.close()


if __name__ == "__main__":
    run_client()
