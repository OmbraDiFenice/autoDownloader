import platform
import unittest
from unittest.mock import patch
import downloaders
import xmlrpc.client
import os.path
from tests.utils import get_binary_file
from jsonschema.exceptions import ValidationError


class TestTorrentDownloader(unittest.TestCase):
    DownloaderClass = downloaders.TorrentDownloader

    def test_init_parameter(self):
        spec_tcp = {
            "type": "TorrentDownloader",
            "host": "http://192.168.1.50:80"
        }
        tcp_downloader = self.DownloaderClass(spec_tcp)
        self.assertEqual(tcp_downloader.host, "http://192.168.1.50:80")

        spec_unix = {
            "type": "TorrentDownloader",
            "host": "/tmp/rtorrent/rtorrent.sock"
        }
        unix_downloader = self.DownloaderClass(spec_unix)
        self.assertEqual(unix_downloader.host, "/tmp/rtorrent/rtorrent.sock")

    @patch("socket.socket")
    def test_call_tcp_socket(self, mock_socket):
        mock_socket.return_value.recv.side_effect = [b'ok', b'']

        url = "http://test.url.com/file.torrent"
        dest = "tests/data/downloaders/dest_folder"

        spec = {
            "type": "TorrentDownloader",
            "host": "http://192.168.1.50:80"
        }
        tcp_downloader = self.DownloaderClass(spec)
        file_name = tcp_downloader.download(url, dest)

        self.assertEqual(file_name, "file.torrent")
        self.assert_xmlrpc_request_was_correct(mock_socket, ("192.168.1.50", 80), url, dest)

    @patch("socket.socket")
    def test_tcp_socket_not_called_if_skip_is_true(self, mock_socket):
        mock_socket.return_value.recv.side_effect = [b'ok', b'']

        url = "http://test.url.com/file.torrent"
        dest = "tests/data/downloaders/dest_folder"

        spec = {
            "type": "TorrentDownloader",
            "host": "http://192.168.1.50:80"
        }
        tcp_downloader = self.DownloaderClass(spec)
        tcp_downloader.download(url, dest, skip=True)

        mock_socket.return_value.connect.assert_not_called()
        mock_socket.return_value.send.assert_not_called()
        mock_socket.return_value.recv.assert_not_called()
        mock_socket.return_value.close.assert_not_called()

    @unittest.skipIf(platform.system() == "Windows", "Unix sockets not available on Windows")
    @patch("socket.socket")
    def test_call_unix_socket(self, mock_socket):
        mock_socket.return_value.recv.side_effect = [b'ok', b'']

        url = "http://test.url.com/file.torrent"
        dest = "tests/data/downloaders/dest_folder"

        spec = {
            "type": "TorrentDownloader",
            "host": "/tmp/rtorrent/rtorrent.sock"
        }
        tcp_downloader = self.DownloaderClass(spec)
        file_name = tcp_downloader.download(url, dest)

        self.assertEqual(file_name, "file.torrent")
        self.assert_xmlrpc_request_was_correct(mock_socket, "/tmp/rtorrent/rtorrent.sock", url, dest)

    @staticmethod
    def assert_xmlrpc_request_was_correct(mock_socket, host, url, dest):
        mock_socket.return_value.connect.assert_called_once_with(host)
        mock_socket.return_value.close.assert_called_once()
        method = "load.start"
        params = (method, "", url, 'd.directory.set="{}"'.format(dest))
        data = xmlrpc.client.dumps(params[1:], methodname=method)
        header = "CONTENT_LENGTH\x00{}\x00SCGI\x001\x00".format(len(data))
        expected_message = "{}:{},{}".format(len(header), header, data)
        encoded_expected_message = expected_message.encode("utf-8")
        mock_socket.return_value.send.assert_called_once_with(encoded_expected_message)


class TestLoggingTorrentDownloader(TestTorrentDownloader):
    DownloaderClass = downloaders.LoggingTorrentDownloader


class TestHttpDownloader(unittest.TestCase):
    DownloaderClass = downloaders.HttpDownloader

    def setUp(self):
        self.dest_dir = "tests/data"
        self.dest_file_name = "test_file.zip"

    def tearDown(self):
        if hasattr(self, "dest_path") and os.path.isfile(self.dest_path):
            os.remove(self.dest_path)

    def assert_file_downloaded_through_get(self, mock_get, mock_post):
        mock_post.assert_not_called()
        mock_get.assert_called_once()

    def assert_downloaded_with_expected_filename(self, expected_filename=None):
        if expected_filename is None:
            expected_filename = self.dest_file_name
        expected_filename = expected_filename.replace("\"", "")
        expected_filename = expected_filename.replace("'", "")
        expected_path = self.dest_path = os.path.join(self.dest_dir, expected_filename)
        self.assertTrue(os.path.isfile(expected_path))

    def assert_file_downloaded_through_post(self, mock_get, mock_post):
        mock_get.assert_not_called()
        mock_post.assert_called_once()

    def create_downloader(self, method):
        spec = {
            "type": "HttpDownloader",
            "method": method
        }
        return self.DownloaderClass(spec)

    def test_download_with_wrong_method(self):
        self.assertRaises(ValidationError, self.create_downloader, "UNSUPPORTED_METHOD")

    @patch("requests.get", side_effect=get_binary_file(name_in_header=True, filename='"[DCFS] DC 100.zip"'))
    @patch("requests.post")
    def test_download_quoted_filename_from_http_headers(self, mock_post, mock_get):
        downloader = self.create_downloader("GET")
        file_name = downloader.download("http://test.url.com/test_not_file_name.zip", self.dest_dir)
        expected_filename = "[DCFS] DC 100.zip"
        self.assertEqual(file_name, expected_filename)
        self.assert_file_downloaded_through_get(mock_get, mock_post)
        self.assert_downloaded_with_expected_filename(expected_filename='"[DCFS] DC 100.zip"')

    @patch("requests.get", side_effect=get_binary_file(name_in_header=True))
    @patch("requests.post")
    def test_download_with_get_filename_from_http_headers(self, mock_post, mock_get):
        downloader = self.create_downloader("GET")
        file_name = downloader.download("http://test.url.com/test_not_file_name.zip", self.dest_dir)
        expected_filename = self.dest_file_name
        self.assertEqual(file_name, expected_filename)
        self.assert_file_downloaded_through_get(mock_get, mock_post)
        self.assert_downloaded_with_expected_filename(expected_filename=expected_filename)

    @patch("requests.get", side_effect=get_binary_file(name_in_header=False))
    @patch("requests.post")
    def test_download_with_get_filename_from_url(self, mock_post, mock_get):
        downloader = self.create_downloader("GET")
        file_name = downloader.download("http://test.url.com/test_file.zip", self.dest_dir)
        expected_filename = "test_file.zip"
        self.assertEqual(file_name, expected_filename)
        self.assert_file_downloaded_through_get(mock_get, mock_post)
        self.assert_downloaded_with_expected_filename(expected_filename=expected_filename)

    @patch("requests.get", side_effect=get_binary_file(name_in_header=False))
    @patch("requests.post")
    def test_download_not_triggered_if_skip_is_true(self, mock_post, mock_get):
        downloader = self.create_downloader("GET")
        file_name = downloader.download("http://test.url.com/test_file.zip", self.dest_dir, skip=True)
        expected_filename = "download skipped, no filename available"
        self.assertEqual(file_name, expected_filename)
        mock_get.assert_not_called()
        mock_post.assert_not_called()

    @patch("requests.get")
    @patch("requests.post", side_effect=get_binary_file(name_in_header=True))
    def test_download_with_post_filename_from_http_headers(self, mock_post, mock_get):
        downloader = self.create_downloader("POST")
        file_name = downloader.download("http://test.url.com/test_not_file_name.zip", self.dest_dir)
        expected_filename = self.dest_file_name
        self.assertEqual(file_name, expected_filename)
        self.assert_file_downloaded_through_post(mock_get, mock_post)
        self.assert_downloaded_with_expected_filename(expected_filename=expected_filename)

    @patch("requests.get")
    @patch("requests.post", side_effect=get_binary_file(name_in_header=False))
    def test_download_with_post_filename_from_url(self, mock_post, mock_get):
        downloader = self.create_downloader("POST")
        file_name = downloader.download("http://test.url.com/test_file.zip", self.dest_dir)
        expected_filename = "test_file.zip"
        self.assertEqual(file_name, expected_filename)
        self.assert_file_downloaded_through_post(mock_get, mock_post)
        self.assert_downloaded_with_expected_filename(expected_filename=expected_filename)


class TestLoggingHttpDownloader(TestHttpDownloader):
    DownloaderClass = downloaders.LoggingHttpDownloader


class TestNullDownloader(unittest.TestCase):
    def test_download(self):
        downloader = downloaders.NullDownloader({"type": "NullDownloader"})
        content = downloader.download("any url", "any dest")
        self.assertEqual("fakeFile", content)

    def test_download_if_skip_is_true(self):
        downloader = downloaders.NullDownloader({"type": "NullDownloader"})
        content = downloader.download("any url", "any dest", skip=True)
        self.assertEqual("fakeFile", content)


if __name__ == '__main__':
    unittest.main()
