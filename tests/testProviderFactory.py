import unittest
from providers import RssProvider, HtmlProvider, ProviderFactoryError, create_provider


class TestProviderFactory(unittest.TestCase):
    def test_throw_error_if_no_type_is_specified(self):
        provider_specs = {
            "name": "testProvider",
        }
        self.assertRaisesRegex(ProviderFactoryError, r"Unable to create provider: type not defined",
                               create_provider, provider_specs)

    def test_throw_error_if_specified_type_is_unknown(self):
        provider_specs = {
            "name": "testProvider",
            "type": "unknown"
        }
        self.assertRaisesRegex(ProviderFactoryError, r"Unable to create provider: type 'unknown' not know",
                               create_provider, provider_specs)

    def test_create_rss_provider(self):
        provider_specs = {
            "name": "test provider",
            "type": "rss"
        }
        provider = create_provider(provider_specs)
        self.assertIsInstance(provider, RssProvider)

    def test_create_html_provider(self):
        provider_specs = {
            "name": "test provider",
            "type": "html"
        }
        provider = create_provider(provider_specs)
        self.assertIsInstance(provider, HtmlProvider)


if __name__ == '__main__':
    unittest.main()
