import unittest
from unittest.mock import patch
import requests
from caches import FileCache
from providers import RssProvider


def get_standard_xml():
    with open("tests/data/providers/rss/sample.xml", "rb") as f:
        xml = f.read()
    response = requests.Response()
    response._content = xml
    return response


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

        expected_urls = [
            "https://fixtures/removable.torrent",
            "https://madness/rome.torrent",
            "https://forbidden/describe.torrent",
            "https://give/hello.torrent",
            "https://processed/robots.torrent",
            "https://dayton/percent.torrent",
            "https://corner/conclusions.torrent",
            "https://palestinian/australia.torrent",
            "https://classification/achieving.torrent",
            "https://auditor/hire.torrent",
            "https://regarding/internal.torrent",
            "https://providing/reveal.torrent",
            "https://serum/techniques.torrent",
            "https://household/podcast.torrent",
            "https://concentration/grip.torrent",
            "https://competition/watches.torrent",
            "https://wheat/florida.torrent",
            "https://hook/producer.torrent",
            "https://call/experienced.torrent",
            "https://stupid/nudity.torrent",
            "https://kyle/soonest.torrent",
            "https://detected/mothers.torrent",
            "https://fraser/discusses.torrent",
            "https://damage/mardi.torrent",
            "https://sunset/remained.torrent",
            "https://shannon/comes.torrent",
            "https://protein/hdtv.torrent",
            "https://eugene/exclusion.torrent",
            "https://requesting/importantly.torrent",
            "https://wind/writers.torrent",
            "https://meetings/voted.torrent",
            "https://unsubscribe/rouge.torrent",
            "https://sciences/tradition.torrent",
            "https://trading/paid.torrent",
            "https://antivirus/hamilton.torrent",
            "https://loving/above.torrent",
            "https://steven/external.torrent",
            "https://armor/museum.torrent",
            "https://celebrate/argue.torrent",
            "https://richard/balance.torrent",
            "https://minor/holidays.torrent",
            "https://holdings/concord.torrent",
            "https://angel/football.torrent",
            "https://swim/background.torrent",
            "https://hottest/meant.torrent",
            "https://modems/fuck.torrent",
            "https://injuries/increasing.torrent",
            "https://notices/strong.torrent",
            "https://specifically/thumbnails.torrent",
            "https://millennium/findings.torrent",
        ]
        get_mock.assert_called_once()
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
