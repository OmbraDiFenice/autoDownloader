import unittest
import shutil
import os
from unittest.mock import patch, call
from tests.utils import get_standard_xml
import caches
import downloaders
import providers
import items
from factories import Factory
import platform


class TestItem(unittest.TestCase):
    ItemClass = items.Item

    def setUp(self):
        cache_path = "tests/data/sample_cache"
        shutil.copyfile("tests/data/providers/rss/sample_cache", cache_path)
        self.base_spec = {
            "name": "my item 1",
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
        self.item = self.get_item(self.base_spec)

    def get_item(self, spec):
        # need to explicitly inject a new instance of cache factory to avoid the
        # factory to reuse instances of cache objects created in other tests
        return self.ItemClass(spec, cache_factory=Factory("caches"))

    def tearDown(self):
        if os.path.isfile("tests/data/sample_cache"):
            os.remove("tests/data/sample_cache")

    def test_create_from_config(self):
        self.assertEqual(self.item.name, "my item 1")
        self.assertEqual(self.item.dest_dir, "/home/myUser/downloads")
        self.assertEqual(self.item.global_post_script, None)
        self.assertEqual(self.item.global_pre_script, None)
        self.assertEqual(self.item.pre_download_script, None)
        self.assertEqual(self.item.post_download_script, None)
        self.assertIsInstance(self.item.provider, providers.RssProvider)
        self.assertIsInstance(self.item.cache, caches.FileCache)
        self.assertIsInstance(self.item.downloader, downloaders.TorrentDownloader)

    def test_cache_defaults_to_null_cache(self):
        spec = self.base_spec.copy()
        del spec["cache"]
        self.assertNotIn("cache", spec.keys())

        item = self.ItemClass(spec)

        self.assertIsInstance(item.cache, caches.NullCache)

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
        expected_calls = [call(args, self.item.dest_dir, False) for args in expected_args_list]
        actual_calls = mock_downloader.download.call_args_list
        self.assert_list_content_is_equivalent(actual_calls, expected_calls)

    @patch("requests.get", return_value=get_standard_xml())
    @patch("socket.socket")
    def test_cache_is_updated_after_download(self, mock_socket, _):
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
            cache_from_file = cache_factory.create(self.base_spec["cache"])
            self.assert_urls_in_cache(cache_from_file, expected_cache_content)

    @patch("requests.get", return_value=get_standard_xml())
    @patch("socket.socket")
    @patch("subprocess.call")
    def test_global_post_script_executed(self, mock_call, mock_socket, _):
        spec = self.base_spec.copy()
        spec["global_post_script"] = "ls -l"
        item = self.get_item(spec)

        self.assertEqual(item.global_post_script, ["ls", "-l"])

        mock_socket.return_value.recv.return_value = b''

        item.download_new_elements()

        expected_calls = [call(["ls", "-l"], cwd=item.dest_dir, env=os.environ)]
        actual_calls = mock_call.call_args_list
        self.assert_list_content_is_equivalent(actual_calls, expected_calls)

    @patch("requests.get", return_value=get_standard_xml())
    @patch("socket.socket")
    @patch("subprocess.call")
    def test_global_pre_script_executed(self, mock_call, mock_socket, _):
        spec = self.base_spec.copy()
        spec["global_pre_script"] = ["ls", "some path"]
        item = self.get_item(spec)

        self.assertEqual(item.global_pre_script, ["ls", "some path"])

        mock_socket.return_value.recv.return_value = b''

        item.download_new_elements()

        expected_calls = [call(["ls", "some path"], cwd=item.dest_dir, env=os.environ)]
        actual_calls = mock_call.call_args_list
        self.assert_list_content_is_equivalent(actual_calls, expected_calls)

    @patch("requests.get", return_value=get_standard_xml())
    @patch("socket.socket")
    @patch("subprocess.call")
    def test_pre_download_script_executed(self, mock_call, mock_socket, _):
        spec = self.base_spec.copy()
        spec["pre_download_script"] = "some_script"
        item = self.get_item(spec)

        self.assertEqual(item.pre_download_script, ["some_script"])

        mock_socket.return_value.recv.return_value = b''

        item.download_new_elements()

        env_call_1 = os.environ.copy()
        env_call_1["AUTODOWNLOADER_URL"] = "https://give/hello.torrent"
        env_call_2 = os.environ.copy()
        env_call_2["AUTODOWNLOADER_URL"] = "https://processed/robots.torrent"
        expected_calls = [
            call(["some_script"], cwd=item.dest_dir, env=env_call_1),
            call(["some_script"], cwd=item.dest_dir, env=env_call_2)
        ]
        actual_calls = mock_call.call_args_list
        self.assert_list_content_is_equivalent(actual_calls, expected_calls)

    @patch("requests.get", return_value=get_standard_xml())
    @patch("socket.socket")
    @patch("subprocess.call")
    def test_post_download_script_executed(self, mock_call, mock_socket, _):
        spec = self.base_spec.copy()
        spec["post_download_script"] = "some_script"
        item = self.get_item(spec)

        self.assertEqual(item.post_download_script, ["some_script"])

        mock_socket.return_value.recv.return_value = b''

        item.download_new_elements()

        env_call_1 = os.environ.copy()
        env_call_1["AUTODOWNLOADER_URL"] = "https://give/hello.torrent"
        env_call_1["AUTODOWNLOADER_FILENAME"] = "hello.torrent"
        env_call_2 = os.environ.copy()
        env_call_2["AUTODOWNLOADER_URL"] = "https://processed/robots.torrent"
        env_call_2["AUTODOWNLOADER_FILENAME"] = "robots.torrent"
        expected_calls = [
            call(["some_script"], cwd=item.dest_dir, env=env_call_1),
            call(["some_script"], cwd=item.dest_dir, env=env_call_2)
        ]
        actual_calls = mock_call.call_args_list
        self.assert_list_content_is_equivalent(actual_calls, expected_calls)

    @unittest.skipIf(platform.system() != "Windows", "Windows shell variable expansion not available on this platform")
    @patch("requests.get", return_value=get_standard_xml())
    @patch("socket.socket")
    @patch("subprocess.call")
    def test_post_download_script_executed_with_windows_expanded_variables(self, mock_call, mock_socket, _):
        spec = self.base_spec.copy()
        spec["post_download_script"] = "some_script %AUTODOWNLOADER_FILENAME%"
        item = self.get_item(spec)

        self.assertEqual(item.post_download_script, ["some_script", "%AUTODOWNLOADER_FILENAME%"])

        mock_socket.return_value.recv.return_value = b''

        item.download_new_elements()

        env_call_1 = os.environ.copy()
        env_call_1["AUTODOWNLOADER_URL"] = "https://give/hello.torrent"
        env_call_1["AUTODOWNLOADER_FILENAME"] = "hello.torrent"
        env_call_2 = os.environ.copy()
        env_call_2["AUTODOWNLOADER_URL"] = "https://processed/robots.torrent"
        env_call_2["AUTODOWNLOADER_FILENAME"] = "robots.torrent"
        expected_calls = [
            call(["some_script", env_call_1["AUTODOWNLOADER_FILENAME"]], cwd=item.dest_dir, env=env_call_1),
            call(["some_script", env_call_2["AUTODOWNLOADER_FILENAME"]], cwd=item.dest_dir, env=env_call_2)
        ]
        actual_calls = mock_call.call_args_list
        self.assert_list_content_is_equivalent(actual_calls, expected_calls)

    def assert_list_content_is_equivalent(self, list1, list2):
        self.assertEqual(len(list2), len(list1))
        for item in list1:
            self.assertIn(item, list2)

    def assert_urls_in_cache(self, cache, expected_cache_content):
        urls_in_cache = [url for url in cache]
        urls_in_cache.sort()
        expected_cache_content_copy = expected_cache_content.copy()
        expected_cache_content_copy.sort()
        self.assertEqual(urls_in_cache, expected_cache_content_copy)


class TestLoggingItem(TestItem):
    ItemClass = items.LoggingItem


if __name__ == '__main__':
    unittest.main()
