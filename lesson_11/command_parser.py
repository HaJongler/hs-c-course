import argparse


class Command(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.__add_arguments()

    def __check_key(self, k):
        if not k.isalnum():
            raise argparse.ArgumentTypeError("must be alphanumeric")
        return k

    def __add_arguments(self):
        subprasers = self.parser.add_subparsers()

        get_parser = subprasers.add_parser("get")
        get_parser.set_defaults(which="get")
        get_parser.add_argument("key", type=self.__check_key)

        put_parser = subprasers.add_parser("put")
        put_parser.set_defaults(which="put")
        put_parser.add_argument("key", type=self.__check_key)
        put_parser.add_argument("value")

        list_parser = subprasers.add_parser("list")
        list_parser.set_defaults(which="list")

    def parse(self, string):
        try:
            return self.parser.parse_args(string.split())
        except SystemExit:
            return False
