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
        return inspect.isclass(cls) and not inspect.isabstract(cls) and base_class in cls.__mro__

    def _get_available_classes(self):
        return inspect.getmembers(sys.modules[self.module], self._is_class_eligible)

    def create(self, spec):
        if "type" not in spec.keys():
            raise FactoryError("Unable to create object: type not defined")

        available_classes = self._get_available_classes()

        new_class_names = ["Logging{}".format(spec["type"]), spec["type"]]
        for new_class_name in new_class_names:
            for available_class_name, available_class in available_classes:
                if available_class_name == new_class_name:
                    return available_class(spec)

        raise FactoryError("Unable to create object: type '{}' not known".format(spec["type"]))


class FactoryError(Exception):
    pass
