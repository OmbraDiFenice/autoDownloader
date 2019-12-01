from caches import AbstractCache
from providers import AbstractProvider
from downloaders import AbstractDownloader
import inspect
import sys


class Factory:
    mapping = {
        "caches": AbstractCache,
        "providers": AbstractProvider,
        "downloaders": AbstractDownloader
    }

    def __init__(self, module):
        self.module = module
        self.__objects_cache__ = []  # contains tuples in the form (spec, cls(spec))

    def _is_class_eligible(self, cls):
        base_class = self.mapping[self.module]
        return inspect.isclass(cls) and not inspect.isabstract(cls) and base_class in cls.__mro__

    def _get_available_classes(self):
        return inspect.getmembers(sys.modules[self.module], self._is_class_eligible)

    def _get_or_create_instance(self, cls, spec):
        cached_obj_list = [cached_obj for cached_obj in self.__objects_cache__ if spec == cached_obj[0]]
        if len(cached_obj_list) > 0:
            return cached_obj_list[0][1]
        else:
            new_obj = cls(spec)
            self.__objects_cache__.append((spec, new_obj))
            return new_obj

    def create(self, spec):
        if "type" not in spec.keys():
            raise FactoryError("Unable to create object: type not defined")

        available_classes = self._get_available_classes()

        new_class_names = ["Logging{}".format(spec["type"]), spec["type"]]
        for new_class_name in new_class_names:
            for available_class_name, available_class in available_classes:
                if available_class_name == new_class_name:
                    return self._get_or_create_instance(available_class, spec)

        raise FactoryError("Unable to create object: type '{}' not known".format(spec["type"]))


class FactoryError(Exception):
    pass
