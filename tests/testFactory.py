import unittest
import os
from factories import Factory, FactoryError
from providers import RssProvider, HtmlProvider
from caches import FileCache, NullCache
from downloaders import TorrentDownloader


class TestFactory(unittest.TestCase):
    def setUp(self):
        self.factories = [
            Factory("providers"),
            Factory("caches"),
            Factory("downloaders")
        ]

    def test_throw_error_if_no_type_is_specified(self):
        for factory in self.factories:
            spec = {}
            self.assertRaisesRegex(FactoryError, r"type not defined",
                                   factory.create, spec)

    def test_throw_error_if_specified_type_is_unknown(self):
        for factory in self.factories:
            spec = {
                "type": "unknown"
            }
            self.assertRaisesRegex(FactoryError, r"type 'unknown' not known",
                                   factory.create, spec)


class TestProviderFactory(unittest.TestCase):
    def setUp(self):
        self.factory = Factory("providers")

    def test_create_rss_provider(self):
        spec = {
            "type": "RssProvider"
        }

        provider = self.factory.create(spec)

        self.assertIsInstance(provider, RssProvider)

    def test_create_html_provider(self):
        spec = {
            "type": "HtmlProvider"
        }

        provider = self.factory.create(spec)

        self.assertIsInstance(provider, HtmlProvider)


class TestCacheFactory(unittest.TestCase):
    def setUp(self):
        self.factory = Factory("caches")

        if os.path.isfile("test_cache"):
            os.remove("test_cache")

    def tearDown(self):
        if os.path.isfile("test_cache"):
            os.remove("test_cache")

    def test_create_file_cache(self):
        spec = {
            "type": "FileCache",
            "path": "test_cache"
        }

        cache = self.factory.create(spec)

        self.assertIsInstance(cache, FileCache)

    def test_create_null_cache(self):
        spec = {
            "type": "NullCache"
        }

        cache = self.factory.create(spec)

        self.assertIsInstance(cache, NullCache)


class TestDownloaderFactory(unittest.TestCase):
    def setUp(self):
        self.factory = Factory("downloaders")

    def test_create_torrent_downloader(self):
        spec = {
            "type": "TorrentDownloader",
            "host": "/tmp/rtorrent/rtorrent.sock"
        }

        downloader = self.factory.create(spec)

        self.assertIsInstance(downloader, TorrentDownloader)


if __name__ == '__main__':
    unittest.main()
