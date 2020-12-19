import unittest
import unittest.mock
import json
import os
from main import build_item_list, load_log_config, load_config, download_all
import items
from jsonschema.exceptions import ValidationError


class TestMain(unittest.TestCase):
    def tearDown(self):
        if os.path.isfile("tests/data/sample_cache"):
            os.remove("tests/data/sample_cache")

    def test_two_items_can_share_file_cache_if_equal(self):
        config = {
            "items": [
                {
                    "name": "item 1",
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
                            "Topic\\..*2\\."
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
                    "name": "item 2",
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
                            "Chapter1"
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

        item_list = build_item_list(config, [])

        self.assertIs(item_list[0].cache, item_list[1].cache)

    def test_filter_items_from_config_by_name(self):
        config = {
            "items": [
                {
                    "name": "item 1",
                    "dest_dir": "some/dest/dir",
                    "provider": {
                        "type": "FileProvider",
                        "path": "some/path",
                    },
                    "downloader": {
                        "type": "NullDownloader"
                    }
                },
                {
                    "name": "item 2",
                    "dest_dir": "some/dest/dir",
                    "provider": {
                        "type": "FileProvider",
                        "path": "some/path"
                    },
                    "downloader": {
                        "type": "NullDownloader"
                    }
                },
                {
                    "name": "item3",
                    "dest_dir": "some/dest/dir",
                    "provider": {
                        "type": "FileProvider",
                        "path": "some/path"
                    },
                    "downloader": {
                        "type": "NullDownloader"
                    }
                }
            ]
        }

        with self.subTest("name with spaces"):
            item_list = build_item_list(config, ["item 2"])

            self.assertEqual(1, len(item_list))
            self.assertEqual("item 2", item_list[0].name)

        with self.subTest("name without spaces"):
            item_list = build_item_list(config, ["item3"])

            self.assertEqual(1, len(item_list))
            self.assertEqual("item3", item_list[0].name)

        with self.subTest("more than one filter"):
            item_list = build_item_list(config, ["item 1", "item3"])

            self.assertEqual(2, len(item_list))
            self.assertIn("item 1", [item.name for item in item_list])
            self.assertIn("item3", [item.name for item in item_list])

        with self.subTest("no filters"):
            item_list = build_item_list(config, [])
            item_names = [item.name for item in item_list]

            self.assertEqual(3, len(item_list))
            self.assertIn("item 1", item_names)
            self.assertIn("item 2", item_names)
            self.assertIn("item3", item_names)

    @unittest.mock.patch("logging.config.dictConfig")
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

    @unittest.mock.patch("logging.config.dictConfig")
    def test_load_custom_log_configuration(self, mock_dict_config):
        test_log_config = "tests/data/log_configuration.json"
        load_log_config(test_log_config)

        with open(test_log_config, "r") as f:
            expected_log_config = json.load(f)

        mock_dict_config.assert_called_once_with(expected_log_config)

    def test_load_valid_config(self):
        config = load_config("tests/data/valid_config.json")
        with open("tests/data/valid_config.json") as f:
            expected_config = json.load(f)

        self.assertDictEqual(expected_config, config)

    def test_load_invalid_config_http_method(self):
        config_file = '''{
            "items": [
                {
                    "name": "some name",
                    "dest_dir": "some/dir",
                    "downloader": {
                        "type": "HttpDownloader",
                        "method": "unsupported method"
                    },
                    "provider": {
                        "type": "FileProvider",
                        "path": "/some/path"
                    }
                }
            ]
        }'''
        with unittest.mock.patch('main.open', unittest.mock.mock_open(read_data=config_file)):
            self.assertRaises(ValidationError, load_config)

    def test_load_invalid_config_empty_cache(self):
        config_file = '''{
            "items": [
                {
                    "name": "some name",
                    "dest_dir": "some/dir",
                    "downloader": {
                        "type": "HttpDownloader",
                        "method": "GET"
                    },
                    "cache": {},
                    "provider": {
                        "type": "FileProvider",
                        "path": "/some/path"
                    }
                }
            ]
        }'''
        with unittest.mock.patch('main.open', unittest.mock.mock_open(read_data=config_file)):
            self.assertRaises(ValidationError, load_config)

    def test_download_all(self):
        item_list = [unittest.mock.MagicMock(spec=items.Item),
                     unittest.mock.MagicMock(spec=items.Item)]
        download_all(item_list, skip=False)
        for item in item_list:
            item.download_new_elements.assert_called_once_with(False)

    def test_download_all_with_skip(self):
        item_list = [unittest.mock.MagicMock(spec=items.Item),
                     unittest.mock.MagicMock(spec=items.Item)]
        download_all(item_list, skip=True)
        for item in item_list:
            item.download_new_elements.assert_called_once_with(True)


if __name__ == '__main__':
    unittest.main()
