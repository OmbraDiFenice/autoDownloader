import unittest
from providers import Provider


class TestProvider(unittest.TestCase):
    def test_empty_provider(self):
        provider = Provider()
        self.assertIsInstance(provider, Provider)


if __name__ == '__main__':
    unittest.main()
