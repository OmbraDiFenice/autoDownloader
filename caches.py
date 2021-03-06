import os
from abc import ABCMeta, abstractmethod
import logging


class AbstractCache(metaclass=ABCMeta):
    @abstractmethod
    def store(self, element):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass


class NullCache(AbstractCache):
    def __init__(self, spec):
        pass

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


class FileCache(AbstractCache):
    def __init__(self, spec):
        self._list = []
        self.path = spec["path"]
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


class LoggingFileCache(FileCache):
    def __init__(self, spec):
        super().__init__(spec)

    def _load(self):
        logging.info("loading cache from {}".format(self.path))
        return super()._load()

    def store(self, element):
        logging.debug("storing element {} in cache".format(element))
        return super().store(element)

    def clear(self):
        logging.debug("clearing in-memory cache")
        return super().clear()

    def save(self):
        logging.debug("saving in-memory cache to file {}".format(self.path))
        return super().save()
