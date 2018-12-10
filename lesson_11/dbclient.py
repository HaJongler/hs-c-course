import socket

from .command_parser import Command

DEFAULT_SERVER, DEFAULT_PORT = '127.0.0.1', 1111


class Client(object):
    def __init__(self):
        self.command_parser = Command()
        self.s = None

    def __enter__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((DEFAULT_SERVER, DEFAULT_PORT))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.s.close()

    def run(self):
        while True:
            command = raw_input('> ')
            if self.command_parser.parse(command):
                self.s.sendall(command)


def main():
    with Client() as client:
        client.run()


if __name__ == '__main__':
    main()
