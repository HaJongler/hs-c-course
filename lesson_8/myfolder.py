import os

from myfile import MyFile
from myitem import MyItem


class MyFolder(MyItem):
    def __init__(self, path, parent):
        super(MyFolder, self).__init__(path, parent)

    def load(self):
        folder_items = []
        for item in os.listdir(self.get_path()):
            abspath = os.path.join(self.get_path(), item)
            myitem = MyFile(item, self) if os.path.isfile(abspath) else MyFolder(item, self)
            folder_items.append(myitem)
        return folder_items

    def save(self):
        os.makedirs(self.get_path())
        for item in self.content:
            item.save()
