import jsonschema
import json
import inspect


class SpecValidator:
    def __init__(self, cls):
        if not inspect.isclass(cls):
            raise ValueError("{} is not a class".format(cls))
        self.cls = cls

    def validate(self, spec):
        schema = self._get_schema()
        jsonschema.validate(instance=spec, schema=schema)
        return True

    def _get_schema_file_name(self):
        module = inspect.getmodulename(inspect.getsourcefile(self.cls))
        return "schemas/{}/{}.json".format(module, self.cls.__name__)

    def _get_schema(self):
        schema_file = self._get_schema_file_name()
        with open(schema_file, "r") as f:
            return json.load(f)


class SpecValidatorMixin:
    def _validate_spec(self, spec, instance_class=None):
        if instance_class is None:
            instance_class = self.__class__
        validator = SpecValidator(instance_class)
        validator.validate(spec)
