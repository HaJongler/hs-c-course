import os


class MyFile(object):
    def __init__(self, path):
        self.name = os.path.basename(path)
        self.os_data = os.stat(path)
        self.content = self.load(path)

    def load(self, path):
        with open(path, 'rb') as f:
            return f.read()
