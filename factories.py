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

    def _is_class_eligible(self, cls):
        base_class = self.mapping[self.module]
        return inspect.isclass(cls) and not inspect.isabstract(cls) and base_class in cls.__bases__

    def _get_available_classes(self):
        return inspect.getmembers(sys.modules[self.module], self._is_class_eligible)

    def create(self, spec):
        if "type" not in spec.keys():
            raise FactoryError("Unable to create object: type not defined")

        available_caches = self._get_available_classes()

        new_cache_name = spec["type"]
        for available_cache_name, cache_class in available_caches:
            if available_cache_name == new_cache_name:
                return cache_class(spec)

        raise FactoryError("Unable to create object: type '{}' not known".format(spec["type"]))


class FactoryError(Exception):
    pass
