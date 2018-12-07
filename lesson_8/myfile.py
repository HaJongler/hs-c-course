from myitem import MyItem


class MyFile(MyItem):
    def __init__(self, path, parent):
        super(MyFile, self).__init__(path, parent)

    def load(self):
        with open(self.get_path(), 'rb') as f:
            return f.read()

    def save(self):
        with open(self.get_path(), 'wb') as f:
            f.write(self.content)
