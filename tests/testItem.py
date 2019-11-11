import unittest
import shutil
import os
from unittest.mock import patch, call
from tests.utils import get_standard_xml
import caches
import downloaders
import providers
from items import Item
from factories import Factory


class TestItem(unittest.TestCase):
    def setUp(self):
        cache_path = "tests/data/sample_cache"
        shutil.copyfile("tests/data/providers/rss/sample_cache", cache_path)
        self.config = {
            "dest_dir": "/home/myUser/downloads",
            "provider": {
                "type": "RssProvider",
                "url": "https://myrss.com/item1.rss",
                "namespaces": {
                    "ns0": "https://rssns.info"
                },
                "xpaths": {
                    "items": "//item",
                    "url": "//enclosure/@url",
                    "title": "//title"
                },
                "patterns": [
                    "cedar"
                ]
            },
            "cache": {
                "type": "FileCache",
                "path": cache_path
            },
            "downloader": {
                "type": "TorrentDownloader",
                "host": "http://192.168.1.50:80"
            }
        }
        self.item = Item(self.config)

    def tearDown(self):
        if os.path.isfile("tests/data/sample_cache"):
            os.remove("tests/data/sample_cache")

    def test_create_from_config(self):
        self.assertEqual(self.item.dest_dir, "/home/myUser/downloads")
        self.assertIsInstance(self.item.provider, providers.RssProvider)
        self.assertIsInstance(self.item.cache, caches.FileCache)
        self.assertIsInstance(self.item.downloader, downloaders.TorrentDownloader)

    @patch("requests.get", return_value=get_standard_xml())
    @patch("downloaders.TorrentDownloader")
    @patch("socket.socket")
    def test_download_new_elements_dont_download_those_in_cache(self, mock_socket, mock_downloader, _):
        self.item.downloader = mock_downloader
        mock_socket.return_value.recv.return_value = b''

        self.item.download_new_elements()

        expected_args_list = [
            "https://give/hello.torrent",
            "https://processed/robots.torrent",
        ]
        expected_calls = [call(args, self.item.dest_dir) for args in expected_args_list]
        actual_calls = mock_downloader.download.call_args_list
        self.assert_list_content_is_equivalent(actual_calls, expected_calls)

    @patch("requests.get", return_value=get_standard_xml())
    @patch("downloaders.TorrentDownloader")
    @patch("socket.socket")
    def test_cache_is_updated_after_download(self, mock_socket, mock_downloader, _):
        self.item.downloader = mock_downloader
        mock_socket.return_value.recv.return_value = b''

        self.assertEqual(len(self.item.cache), 1)

        self.item.download_new_elements()

        with self.subTest("cache is persisted in memory"):
            expected_cache_content = [
                "https://forbidden/describe.torrent",
                "https://give/hello.torrent",
                "https://processed/robots.torrent",
            ]
            self.assert_urls_in_cache(self.item.cache, expected_cache_content)

        with self.subTest("cache is persisted on disk"):
            cache_factory = Factory("caches")
            cache_from_file = cache_factory.create(self.config["cache"])
            self.assert_urls_in_cache(cache_from_file, expected_cache_content)

    def assert_list_content_is_equivalent(self, list1, list2):
        self.assertEqual(len(list1), len(list2))
        for item in list1:
            self.assertIn(item, list2)

    def assert_urls_in_cache(self, cache, expected_cache_content):
        urls_in_cache = [url for url in cache]
        urls_in_cache.sort()
        expected_cache_content_copy = expected_cache_content.copy()
        expected_cache_content_copy.sort()
        self.assertEqual(urls_in_cache, expected_cache_content_copy)


if __name__ == '__main__':
    unittest.main()
