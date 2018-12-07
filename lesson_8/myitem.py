import os
from abc import ABCMeta, abstractmethod


class MyItem(object):
    __metaclass__ = ABCMeta

    def __init__(self, path, parent):
        self.name = os.path.basename(path)
        self.os_data = os.stat(path)
        self.parent = parent
        self.content = self.load()

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self):
        pass

    def get_path(self):
        if isinstance(self.parent, str):
            return os.path.join(self.parent, self.name)
        return os.path.join(self.parent.get_path(), self.name)
