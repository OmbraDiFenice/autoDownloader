import unittest
from items import Item
import providers
import downloaders
import caches


class TestItem(unittest.TestCase):
    def test_create_from_config(self):
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
                "type": "NullCache"
            },
            "downloader": {
                "type": "TorrentDownloader",
                "host": "/home/myUser/rtorrent/.session/.rtorrent.sock"
            }
        }
        item = Item(config)

        self.assertEqual(item.dest_dir, config["dest_dir"])
        self.assertIsInstance(item.provider, providers.RssProvider)
        self.assertIsInstance(item.cache, caches.NullCache)
        self.assertIsInstance(item.downloader, downloaders.TorrentDownloader)


if __name__ == '__main__':
    unittest.main()
