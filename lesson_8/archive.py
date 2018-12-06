import pickle

from myfile import MyFile


class Archive(object):
    def __init__(self, data):
        self.data = data

    @classmethod
    def create_from_list(cls, *files):
        return cls([MyFile(fyle) for fyle in files])

    @classmethod
    def load_from_file(cls, path):
        with open(path, 'rb') as f:
            return cls(pickle.load(f))

    def save(self, name):
        with open(name, 'wb') as f:
            pickle.dump(self.data, f, protocol=2)

    def extract(self):
        for myfile in self.data:
            with open(myfile.name, 'wb') as f:
                f.write(myfile.content)

    def list_contents(self):
        for myfile in self.data:
            print(myfile.name)
