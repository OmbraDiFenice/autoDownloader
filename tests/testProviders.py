import unittest
from unittest.mock import patch
from tests.utils import get_standard_xml, get_standard_html
from factories import Factory


class TestRssProvider(unittest.TestCase):
    def setUp(self):
        self.factory = Factory("providers")
        self.spec = {
            "type": "RssProvider",
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
        urls_sorted = urls.copy()
        urls_sorted.sort()
        expected_urls_sorted = expected_urls.copy()
        expected_urls_sorted.sort()
        self.assertEqual(urls_sorted, expected_urls_sorted)

    def test_default_parameters(self):
        minimal_spec = {
            "type": "RssProvider",
            "url": "http://something/feed.xml",
            "xpaths": {
                "items": "//item",
                "url": "//enclosure/@url",
                "title": "//title"
            }
        }
        provider = self.factory.create(minimal_spec)

        self.assertEqual(provider.namespaces, {})
        self.assertEqual(provider.patterns, [".*"])

    def test_empty_pattern_list_defaults_to_match_all(self):
        self.spec["patterns"] = []
        provider = self.factory.create(self.spec)

        self.assertEqual(provider.patterns, [".*"])

    def test_create_provider(self):
        provider = self.factory.create(self.spec)

        self.assertEqual(provider.url, self.spec["url"])
        self.assertEqual(provider.namespaces, self.spec["namespaces"])
        self.assertEqual(provider.items_xpath, self.spec["xpaths"]["items"])
        self.assertEqual(provider.url_xpath, self.spec["xpaths"]["url"])
        self.assertEqual(provider.title_xpath, self.spec["xpaths"]["title"])
        self.assertEqual(provider.patterns, self.spec["patterns"])

    @patch("requests.get", return_value=get_standard_xml())
    def test_get_urls_with_default_pattern(self, get_mock):
        self.spec.pop("patterns")
        provider = self.factory.create(self.spec)

        urls = provider.get_urls()

        get_mock.assert_called_once()
        with open("tests/data/providers/rss/sample_urls.txt", "r") as f:
            expected_urls = [line.strip() for line in f.readlines()]
        self.assert_url_list_matches(urls, expected_urls)

    @patch("requests.get", return_value=get_standard_xml())
    def test_get_urls_with_custom_pattern(self, get_mock):
        self.spec["patterns"] = ["cedar"]
        provider = self.factory.create(self.spec)

        urls = provider.get_urls()

        expected_urls = [
            "https://forbidden/describe.torrent",
            "https://give/hello.torrent",
            "https://processed/robots.torrent",
        ]
        get_mock.assert_called_once()
        self.assert_url_list_matches(urls, expected_urls)


class TestHtmlProvider(unittest.TestCase):
    def setUp(self):
        self.factory = Factory("providers")

    def assert_url_list_matches(self, urls, expected_urls):
        self.assertIsInstance(urls, (list, tuple))
        self.assertIsInstance(expected_urls, (list, tuple))
        urls_sorted = urls.copy()
        urls_sorted.sort()
        expected_urls_sorted = expected_urls.copy()
        expected_urls_sorted.sort()
        self.assertEqual(urls_sorted, expected_urls_sorted)

    @patch("requests.get", return_value=get_standard_html())
    def test_get_urls_according_to_xpath(self, get_mock):
        spec = {
            "type": "HtmlProvider",
            "url": "http://my.awesome.site/page1",
            "xpath": "//*[@id='post-271']/div/table/tbody/tr/td[2]/a/@href"
        }
        with open("tests/data/providers/html/sample_urls.txt", "r") as f:
            expected_urls = [url.strip() for url in f.readlines()]

        provider = self.factory.create(spec)

        urls = provider.get_urls()

        get_mock.assert_called_once()
        self.assertEqual((spec["url"],), get_mock.call_args[0])

        self.assert_url_list_matches(urls, expected_urls)


class TestFileProvider(unittest.TestCase):
    def test_get_urls_from_specified_file(self):
        spec = {
            "type": "FileProvider",
            "path": "tests/data/providers/file/source.txt"
        }
        provider = Factory("providers").create(spec)

        expected_urls = [
            "https://cdn.somedomain.com/elem_1.mp4",
            "https://cdn.somedomain.com/elem_2.mp4"
        ]

        urls = provider.get_urls()

        self.assertEqual(urls, expected_urls)


if __name__ == '__main__':
    unittest.main()
