import os


class Cache:
    pass


class NullCache(Cache):
    def store(self, element):
        pass

    def clear(self):
        pass

    def save(self):
        pass

    def __len__(self):
        return 0

    def __iter__(self):
        return [].__iter__()


class FileCache(Cache):
    def __init__(self, path):
        self._list = []
        self.path = path
        self._load()

    def _load(self):
        if not os.path.isfile(self.path):
            open(self.path, "w").close()
        else:
            with open(self.path, "r") as f:
                self._list = [elem.strip() for elem in f.readlines()]

    def store(self, element):
        self._list.append(element)

    def clear(self):
        self._list = []

    def save(self):
        with open(self.path, "w") as f:
            f.writelines([line if line.endswith('\n') else line + '\n' for line in self._list])

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return self._list.__iter__()
