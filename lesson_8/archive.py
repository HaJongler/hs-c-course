import os
import pickle

from myfile import MyFile
from myfolder import MyFolder


class Archive(object):
    def __init__(self, data):
        self.data = data

    @classmethod
    def create_from_list(cls, *paths):
        data = []
        for path in paths:
            abspath = os.path.abspath(path)
            data.append(MyFile(abspath, os.path.dirname(abspath))
                        if os.path.isfile(abspath)
                        else MyFolder(abspath, os.path.dirname(abspath)))
        return cls(data)

    @classmethod
    def load_from_file(cls, path):
        with open(path, 'rb') as f:
            return cls(pickle.load(f))

    def save(self, name):
        with open(name, 'wb') as f:
            pickle.dump(self.data, f, protocol=2)

    def extract(self):
        for myitem in self.data:
            myitem.parent = '.'
            myitem.save()

    def list_contents(self):
        for myfile in self.data:
            print(myfile.name)
