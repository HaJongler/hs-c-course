import os

import pandas as pd

from .command_parser import Command

DATA_FILE = 'mydb.data'


class Server(object):
    def __init__(self):
        self.command_parser = Command()
        self.db = self.__load_db()

    def __load_db(self):
        if os.path.exists(DATA_FILE):
            return pd.read_csv(DATA_FILE)
        os.mknod(DATA_FILE)
        return pd.DataFrame(columns=['key', 'value'])

    def run(self):
        while True:
            pass


def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()
