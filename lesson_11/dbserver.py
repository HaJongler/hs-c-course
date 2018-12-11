import json
import os
import socket
import sys
from threading import Thread

from command_parser import Command

DATA_FILE = 'mydb.data'
HOST, PORT = '127.0.0.1', 1111


class Server(object):
    def __init__(self):
        self.command_parser = Command()
        self.db = self.__load_db()
        self.s = None

    def __enter__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, PORT))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.s.close()
        with open(DATA_FILE, 'wb') as f:
            f.write(json.dumps(self.db))

    def __load_db(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'rb') as f:
                return json.loads(f.read())
        open(DATA_FILE, 'wb').close()
        return dict()

    def client_thread(self, connection, address):
        max_buffer_size = 5120
        while True:
            try:
                client_input = self.receive_input(connection, max_buffer_size)
                print "Received command: {}".format(client_input)
                response = self.process_input(client_input)
                connection.send(response.encode("utf8"))
            except:
                connection.close()

    def receive_input(self, connection, max_buffer_size):
        client_input = connection.recv(max_buffer_size)
        client_input_size = sys.getsizeof(client_input)

        if client_input_size > max_buffer_size:
            print("The input size is greater than expected {}".format(client_input_size))

        decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
        return decoded_input

    def process_input(self, input_str):
        cmd = self.command_parser.parse(input_str)
        if cmd.which == "get":
            return self.db.get(cmd.key, "Key doesn't exist!")
        elif cmd.which == "put":
            self.db[cmd.key] = cmd.value
            return "Success"
        else:
            return ", ".join(self.db.keys())

    def run(self):
        print "Starting server..."
        self.s.listen(5)  # queue up to 5 requests
        while True:
            connection, address = self.s.accept()
            print "Accepting new connection from client at {}".format(str(address[0]))
            try:
                Thread(target=self.client_thread, args=(connection, address)).start()
            except:
                print("Thread did not start.")


def main():
    with Server() as server:
        server.run()


if __name__ == '__main__':
    main()
