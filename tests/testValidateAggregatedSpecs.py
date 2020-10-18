import unittest
import jsonschema
import json
import os.path
from utils import load_json_schema


class TestValidateAggregatedSpecs(unittest.TestCase):
    def test_load_jsonschema_with_cross_file_references_working(self):
        main_schema = load_json_schema(os.path.join("schemas", "main.json"))

        with open("tests/data/valid_config.json", "r") as f:
            input_json = json.load(f)

        error = False
        try:
            jsonschema.validate(instance=input_json, schema=main_schema)
        except jsonschema.ValidationError:
            error = True

        self.assertFalse(error, "jsonschema validation of a valid json failed!")


if __name__ == '__main__':
    unittest.main()
