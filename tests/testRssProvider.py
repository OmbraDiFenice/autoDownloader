import unittest
from unittest.mock import patch
from providers import RssProvider
from tests.utils import get_standard_xml


class TestRssProvider(unittest.TestCase):
    def setUp(self):
        self.spec = {
            "type": "rss",
            "url": "http://something/feed.xml",
            "xpaths": {
                "items": "//item",
                "url": "//enclosure/@url",
                "title": "//title"
            },
            "namespaces": {},
            "patterns": ["some_regex"],
            "dest_dir": "download/dir"
        }

    def assert_url_list_matches(self, urls, expected_urls):
        urls.sort()
        expected_urls.sort()
        self.assertEqual(urls, expected_urls)

    def test_default_parameters(self):
        minimal_spec = {
            "type": "rss",
            "url": "http://something/feed.xml",
            "xpaths": {
                "items": "//item",
                "url": "//enclosure/@url",
                "title": "//title"
            }
        }
        provider = RssProvider(minimal_spec)

        self.assertEqual(provider.namespaces, {})
        self.assertEqual(provider.patterns, [".*"])

    def test_empty_pattern_list_defaults_to_match_all(self):
        self.spec["patterns"] = []
        provider = RssProvider(self.spec)

        self.assertEqual(provider.patterns, [".*"])

    def test_create_provider(self):
        provider = RssProvider(self.spec)

        self.assertEqual(provider.url, self.spec["url"])
        self.assertEqual(provider.namespaces, self.spec["namespaces"])
        self.assertEqual(provider.items_xpath, self.spec["xpaths"]["items"])
        self.assertEqual(provider.url_xpath, self.spec["xpaths"]["url"])
        self.assertEqual(provider.title_xpath, self.spec["xpaths"]["title"])
        self.assertEqual(provider.patterns, self.spec["patterns"])

    @patch("requests.get", return_value=get_standard_xml())
    def test_get_urls_with_default_pattern(self, get_mock):
        self.spec.pop("patterns")
        provider = RssProvider(self.spec)

        urls = provider.get_urls()

        get_mock.assert_called_once()
        with open("tests/data/providers/rss/sample_urls.txt", "r") as f:
            expected_urls = [line.strip() for line in f.readlines()]
        self.assert_url_list_matches(urls, expected_urls)

    @patch("requests.get", return_value=get_standard_xml())
    def test_get_urls_with_custom_pattern(self, get_mock):
        self.spec["patterns"] = ["cedar"]
        provider = RssProvider(self.spec)

        urls = provider.get_urls()

        expected_urls = [
            "https://forbidden/describe.torrent",
            "https://give/hello.torrent",
            "https://processed/robots.torrent",
        ]
        get_mock.assert_called_once()
        self.assert_url_list_matches(urls, expected_urls)


if __name__ == '__main__':
    unittest.main()
