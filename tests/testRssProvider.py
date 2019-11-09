import unittest
from unittest.mock import patch
from providers import create_provider
import requests
from caches import FileCache


def get_standard_xml():
    with open("tests/data/providers/rss/sample.xml", "rb") as f:
        xml = f.read()
    response = requests.Response()
    response._content = xml
    return response


class TestRssProvider(unittest.TestCase):
    def test_create_provider(self):
        spec = {
            "type": "rss",
            "url": "",
            "xpaths": {
                "items": "//item",
                "url": "//url",
                "title": "//title"
            },
            "namespaces": {},
            "patterns": [],
            "dest_dir": "download/dir"
        }
        provider = create_provider(spec)

        self.assertEqual(provider.url, spec["url"])
        self.assertEqual(provider.namespaces, spec["namespaces"])
        self.assertEqual(provider.items_xpath, spec["xpaths"]["items"])
        self.assertEqual(provider.url_xpath, spec["xpaths"]["url"])
        self.assertEqual(provider.title_xpath, spec["xpaths"]["title"])
        self.assertEqual(provider.patterns, spec["patterns"])
        self.assertEqual(provider.dest_dir, spec["dest_dir"])

    @patch("requests.get", return_value=get_standard_xml())
    def test_get_urls_with_empty_cache_and_default_pattern(self, mock):
        spec = {
            "type": "rss",
            "url": "",
            "xpaths": {
                "items": "//item",
                "url": "//enclosure/@url",
                "title": "//title"
            },
            "namespaces": {}
        }
        provider = create_provider(spec)
        urls = provider.get_urls()

        mock.assert_called_once()
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
        self.assertEqual(urls, expected_urls)

    @patch("requests.get", return_value=get_standard_xml())
    def test_get_urls_with_empty_cache_and_pattern(self, mock):
        spec = {
            "type": "rss",
            "url": "",
            "xpaths": {
                "items": "//item",
                "url": "//enclosure/@url",
                "title": "//title"
            },
            "namespaces": {},
            "patterns": [
                "cedar"
            ]
        }
        provider = create_provider(spec)
        urls = provider.get_urls()

        expected_urls = [
            "https://forbidden/describe.torrent",
            "https://give/hello.torrent",
            "https://processed/robots.torrent",
        ]
        urls.sort()
        expected_urls.sort()
        self.assertEqual(urls, expected_urls)

    @patch("requests.get", return_value=get_standard_xml())
    def test_get_urls_with_cached_entries_and_pattern(self, mock):
        spec = {
            "type": "rss",
            "url": "",
            "xpaths": {
                "items": "//item",
                "url": "//enclosure/@url",
                "title": "//title"
            },
            "namespaces": {},
            "patterns": [
                "cedar"
            ]
        }
        cache = FileCache("tests/data/providers/rss/sample_cache")
        provider = create_provider(spec, cache=cache)
        urls = provider.get_urls()

        expected_urls = [
            "https://give/hello.torrent",
            "https://processed/robots.torrent",
        ]
        urls.sort()
        expected_urls.sort()
        self.assertEqual(urls, expected_urls)


if __name__ == '__main__':
    unittest.main()
