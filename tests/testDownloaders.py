import platform
import unittest
from unittest.mock import patch
from downloaders import TorrentDownloader
import xmlrpc.client
from factories import Factory
import os.path
from tests.utils import get_binary_file


class TestTorrentDownloader(unittest.TestCase):
    def test_init_parameter(self):
        spec_tcp = {
            "type": "TorrentDownloader",
            "host": "http://192.168.1.50:80"
        }
        tcp_downloader = TorrentDownloader(spec_tcp)
        self.assertEqual(tcp_downloader.host, "http://192.168.1.50:80")

        spec_unix = {
            "type": "TorrentDownloader",
            "host": "/tmp/rtorrent/rtorrent.sock"
        }
        unix_downloader = TorrentDownloader(spec_unix)
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
        tcp_downloader = TorrentDownloader(spec)
        tcp_downloader.download(url, dest)

        self.assert_xmlrpc_request_was_correct(mock_socket, ("192.168.1.50", 80), url, dest)

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
        tcp_downloader = TorrentDownloader(spec)
        tcp_downloader.download(url, dest)

        self.assert_xmlrpc_request_was_correct(mock_socket, "/tmp/rtorrent/rtorrent.sock", url, dest)

    @staticmethod
    def assert_xmlrpc_request_was_correct(mock_socket, host, url, dest):
        mock_socket.return_value.connect.assert_called_once_with(host)
        mock_socket.return_value.close.assert_called_once()
        method = "load.start"
        params = (method, "", url, "d.directory.set={}".format(dest))
        data = xmlrpc.client.dumps(params[1:], methodname=method)
        header = "CONTENT_LENGTH\x00{}\x00SCGI\x001\x00".format(len(data))
        expected_message = "{}:{},{}".format(len(header), header, data)
        encoded_expected_message = expected_message.encode("utf-8")
        mock_socket.return_value.send.assert_called_once_with(encoded_expected_message)


class TestHttpDownloader(unittest.TestCase):
    def setUp(self):
        self.factory = Factory("downloaders")
        self.dest_dir = "tests/data"
        self.dest_file_name = "test_file.zip"

    def tearDown(self):
        if os.path.isfile(self.dest_path):
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
        self.assertIn(method, ["GET", "POST"])
        spec = {
            "type": "HttpDownloader",
            "method": method
        }
        return self.factory.create(spec)

    @patch("requests.get", side_effect=get_binary_file(name_in_header=True, filename='"[DCFS] DC 100.zip"'))
    @patch("requests.post")
    def test_download_quoted_filename_from_http_headers(self, mock_post, mock_get):
        downloader = self.create_downloader("GET")
        downloader.download("http://test.url.com/test_not_file_name.zip", self.dest_dir)
        self.assert_file_downloaded_through_get(mock_get, mock_post)
        self.assert_downloaded_with_expected_filename(expected_filename='"[DCFS] DC 100.zip"')

    @patch("requests.get", side_effect=get_binary_file(name_in_header=True))
    @patch("requests.post")
    def test_download_with_get_filename_from_http_headers(self, mock_post, mock_get):
        downloader = self.create_downloader("GET")
        downloader.download("http://test.url.com/test_not_file_name.zip", self.dest_dir)
        self.assert_file_downloaded_through_get(mock_get, mock_post)
        self.assert_downloaded_with_expected_filename()

    @patch("requests.get", side_effect=get_binary_file(name_in_header=False))
    @patch("requests.post")
    def test_download_with_get_filename_from_url(self, mock_post, mock_get):
        downloader = self.create_downloader("GET")
        downloader.download("http://test.url.com/test_file.zip", self.dest_dir)
        self.assert_file_downloaded_through_get(mock_get, mock_post)
        self.assert_downloaded_with_expected_filename()

    @patch("requests.get")
    @patch("requests.post", side_effect=get_binary_file(name_in_header=True))
    def test_download_with_post_filename_from_http_headers(self, mock_post, mock_get):
        downloader = self.create_downloader("POST")
        downloader.download("http://test.url.com/test_not_file_name.zip", self.dest_dir)
        self.assert_file_downloaded_through_post(mock_get, mock_post)
        self.assert_downloaded_with_expected_filename()

    @patch("requests.get")
    @patch("requests.post", side_effect=get_binary_file(name_in_header=False))
    def test_download_with_post_filename_from_url(self, mock_post, mock_get):
        downloader = self.create_downloader("POST")
        downloader.download("http://test.url.com/test_file.zip", self.dest_dir)
        self.assert_file_downloaded_through_post(mock_get, mock_post)
        self.assert_downloaded_with_expected_filename()


if __name__ == '__main__':
    unittest.main()
