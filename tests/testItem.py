import unittest
from unittest.mock import patch, call
from tests.testRssProvider import get_standard_xml
import caches
import downloaders
import providers
from items import Item


class TestItem(unittest.TestCase):
    def setUp(self):
        config = {
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
                "path": "tests/data/providers/rss/sample_cache"
            },
            "downloader": {
                "type": "TorrentDownloader",
                "host": "http://192.168.1.50:80"
            }
        }
        self.item = Item(config)

    def test_create_from_config(self):
        self.assertEqual(self.item.dest_dir, "/home/myUser/downloads")
        self.assertIsInstance(self.item.provider, providers.RssProvider)
        self.assertIsInstance(self.item.cache, caches.FileCache)
        self.assertIsInstance(self.item.downloader, downloaders.TorrentDownloader)

    @patch("requests.get", return_value=get_standard_xml())
    @patch("downloaders.TorrentDownloader")
    @patch("socket.socket")
    def test_download_new_elements_dont_download_those_in_cache(self, mock_socket, mock_downloader, mock_get):
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

    @staticmethod
    def assert_list_content_is_equivalent(list1, list2):
        for item in list1:
            if item not in list2:
                raise AssertionError("item {} not found in {}".format(item, list2))


if __name__ == '__main__':
    unittest.main()
