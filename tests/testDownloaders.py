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
        dest_file_name = "temp_filename"
        self.dest_path = os.path.join(self.dest_dir, dest_file_name)

    def tearDown(self):
        if os.path.isfile(self.dest_path):
            os.remove(self.dest_path)

    @patch("requests.get", side_effect=get_binary_file)
    @patch("requests.post")
    def test_download_with_get(self, mock_post, mock_get):
        spec = {
            "type": "HttpDownloader",
            "method": "GET"
        }
        downloader = self.factory.create(spec)

        url = "http://test.url.com/test_file.zip"
        downloader.download(url, self.dest_dir)

        mock_post.assert_not_called()
        mock_get.assert_called_once()

        self.assertTrue(os.path.isfile(self.dest_path))


if __name__ == '__main__':
    unittest.main()
