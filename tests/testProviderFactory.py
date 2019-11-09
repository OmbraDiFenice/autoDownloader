import unittest
from providers import ProviderFactory, RssProvider, HtmlProvider, ProviderFactoryError


class TestProviderFactory(unittest.TestCase):
    def test_throw_error_if_no_type_is_specified(self):
        provider_specs = {
            "name": "testProvider",
        }

        provider_factory = ProviderFactory()
        self.assertRaisesRegex(ProviderFactoryError, r"Unable to create provider: type not defined",
                               provider_factory.create, provider_specs)

    def test_throw_error_if_specified_type_is_unknown(self):
        provider_specs = {
            "name": "testProvider",
            "type": "unknown"
        }

        provider_factory = ProviderFactory()
        self.assertRaisesRegex(ProviderFactoryError, r"Unable to create provider: type 'unknown' not know",
                               provider_factory.create, provider_specs)

    def test_create_rss_provider(self):
        provider_specs = {
            "name": "test provider",
            "type": "rss"
        }

        provider_factory = ProviderFactory()
        provider = provider_factory.create(provider_specs)
        self.assertIsInstance(provider, RssProvider)

    def test_create_html_provider(self):
        provider_specs = {
            "name": "test provider",
            "type": "html"
        }

        provider_factory = ProviderFactory()
        provider = provider_factory.create(provider_specs)
        self.assertIsInstance(provider, HtmlProvider)


if __name__ == '__main__':
    unittest.main()
