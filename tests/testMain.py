import unittest
import json
from unittest.mock import patch
import os
from main import build_item_list, load_log_config


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

    @patch("logging.config.dictConfig")
    def test_load_default_log_configuration(self, mock_dict_config):
        load_log_config("nonexistent_log_configuration.json")

        default_log_config = {
            'version': 1,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard'
                }
            },
            'loggers': {
                '': {
                    'handlers': ['console'],
                    'level': 'DEBUG'
                }
            }
        }
        mock_dict_config.assert_called_once_with(default_log_config)

    @patch("logging.config.dictConfig")
    def test_load_custom_log_configuration(self, mock_dict_config):
        test_log_config = "tests/data/log_configuration.json"
        load_log_config(test_log_config)

        with open(test_log_config, "r")  as f:
            expected_log_config = json.load(f)

        mock_dict_config.assert_called_once_with(expected_log_config)


if __name__ == '__main__':
    unittest.main()
