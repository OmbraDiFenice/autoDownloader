import unittest
import os
from main import build_item_list


class TestMain(unittest.TestCase):
    def tearDown(self):
        if os.path.isfile("tests/data/sample_cache"):
            os.remove("tests/data/sample_cache")

    def test_two_items_can_share_file_cache_if_equal(self):
        config = {
            "items": [
                {
                    "dest_dir": "/home/myUser/nas/item1",
                    "provider": {
                        "type": "RssProvider",
                        "url": "https://some.url/rss",
                        "namespaces": {
                            "ns": "https://somerss.url"
                        },
                        "xpaths": {
                            "items": "//item",
                            "url": "//enclosure/@url",
                            "title": "//title"
                        },
                        "patterns": [
                            "Topic1"
                        ]
                    },
                    "cache": {
                        "type": "FileCache",
                        "path": "tests/data/sample_cache"
                    },
                    "downloader": {
                        "type": "TorrentDownloader",
                        "host": "http://192.168.1.50:80"
                    }
                },
                {
                    "dest_dir": "/home/myUser/nas/item2",
                    "provider": {
                        "type": "RssProvider",
                        "url": "https://my.address.to/rss.php?categories=catA",
                        "namespaces": {
                            "ns": "https://my.rss.namespace.url"
                        },
                        "xpaths": {
                            "title": "/title",
                            "items": "//item",
                            "url": "/link"
                        },
                        "patterns": [
                            "topic.*1",
                            "topic\\..*9\\.*"
                        ]
                    },
                    "cache": {
                        "type": "FileCache",
                        "path": "tests/data/sample_cache"
                    },
                    "downloader": {
                        "type": "TorrentDownloader",
                        "host": "/home/myUser/rtorrent/.session/.rtorrent.sock"
                    }
                }
            ]
        }

        item_list = build_item_list(config)

        self.assertIs(item_list[0].cache, item_list[1].cache)


if __name__ == '__main__':
    unittest.main()
