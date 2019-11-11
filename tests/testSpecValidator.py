import unittest
import jsonschema
from validators import SpecValidator
import caches
import downloaders


class TestSpecValidator(unittest.TestCase):
    def test_validator_can_only_be_constructed_with_a_class(self):
        with self.subTest("create with string"):
            self.assertRaises(ValueError, SpecValidator, "string")

        with self.subTest("create with bool"):
            self.assertRaises(ValueError, SpecValidator, True)

        with self.subTest("create with int"):
            self.assertRaises(ValueError, SpecValidator, 4)

        with self.subTest("create with float"):
            self.assertRaises(ValueError, SpecValidator, 4.4)

        with self.subTest("create with function"):
            self.assertRaises(ValueError, SpecValidator, lambda x: x)

        with self.subTest("create with class"):
            try:
                SpecValidator(caches.NullCache)
            except Exception:
                raise AssertionError("SpecValidator should be created passing a class")

    def test_validate_valid_file_cache(self):
        spec = {
            "type": "FileCache",
            "path": "some/file/path"
        }
        validator = SpecValidator(caches.FileCache)
        self.assertTrue(validator.validate(spec))

    def test_validate_invalid_file_cache(self):
        spec = {}
        validator = SpecValidator(caches.FileCache)
        self.assertRaises(jsonschema.ValidationError, validator.validate, spec)

    def test_validate_valid_null_cache(self):
        spec = {
            "type": "NullCache"
        }
        validator = SpecValidator(caches.NullCache)
        self.assertTrue(validator.validate(spec))

    def test_validator_can_validate_any_class(self):
        spec = {
            "type": "TorrentDownloader",
            "host": "/test/socket"
        }
        validator = SpecValidator(downloaders.TorrentDownloader)
        self.assertTrue(validator.validate(spec))


if __name__ == '__main__':
    unittest.main()
