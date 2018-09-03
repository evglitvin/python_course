
import socket
import time


def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 80))
    sock.listen(2)

    conn, addr = sock.accept()
    while True:
        data = conn.recv(1024)
        if data == b'exit\r\n'.lower():
            break
        else:
            print('Recv: {0} from {1}'.format(data, addr))
            conn.send(b'hello\r\n')
        time.sleep(0.0005)

    sock.close()


def run_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect(('localhost', 80))

    sock.send(b'hello world\r\n')
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