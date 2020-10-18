import os.path
import jsonref


def load_json_schema(filename):
    """ Loads the given schema file """

    absolute_path = os.path.join(os.path.dirname(__file__), filename)

    base_path = os.path.dirname(absolute_path)
    base_uri = 'file:///{}/'.format(base_path)

    base_uri = base_uri.replace("\\", "/")

    with open(absolute_path) as schema_file:
        return jsonref.loads(schema_file.read(), base_uri=base_uri, jsonschema=True)
