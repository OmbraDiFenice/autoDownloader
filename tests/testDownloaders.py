import platform
import unittest
from unittest.mock import patch, Mock
from downloaders import TorrentDownloader
import xmlrpc.client


class TestTorrentDownloader(unittest.TestCase):
    def test_init_parameter(self):
        tcp_downloader = TorrentDownloader("http://192.168.1.50:80")
        self.assertEqual(tcp_downloader.host, "http://192.168.1.50:80")

        unix_downloader = TorrentDownloader("/tmp/rtorrent/rtorrent.sock")
        self.assertEqual(unix_downloader.host, "/tmp/rtorrent/rtorrent.sock")

    @patch("socket.socket")
    def test_call_tcp_socket(self, mock_socket):
        mock_socket.return_value.recv.side_effect = ['ok', '']

        url = "http://test.url.com/file.torrent"
        dest = "tests/data/downloaders/dest_folder"

        tcp_downloader = TorrentDownloader("http://192.168.1.50:80")
        tcp_downloader.download(url, dest)

        self.assert_use_socket_for_correct_xmlrpc(mock_socket, ("192.168.1.50", 80), url, dest)

    @unittest.skipIf(platform.system() == "Windows", "Unix sockets not available on Windows")
    @patch("socket.socket")
    def test_call_unix_socket(self, mock_socket):
        mock_socket.return_value.recv.side_effect = ['ok', '']

        url = "http://test.url.com/file.torrent"
        dest = "tests/data/downloaders/dest_folder"

        tcp_downloader = TorrentDownloader("/tmp/rtorrent/rtorrent.sock")
        tcp_downloader.download(url, dest)

        self.assert_use_socket_for_correct_xmlrpc(mock_socket, "/tmp/rtorrent/rtorrent.sock", url, dest)

    def assert_use_socket_for_correct_xmlrpc(self, mock_socket, host, url, dest):
        mock_socket.return_value.connect.assert_called_once_with(host)
        mock_socket.return_value.close.assert_called_once()
        method = "load.start"
        params = (method, "", url, "d.directory.set={}".format(dest))
        data = xmlrpc.client.dumps(params[1:], methodname=method)
        header = "CONTENT_LENGTH\x00{}\x00SCGI\x001\x00".format(len(data))
        expected_message = "{}:{},{}".format(len(header), header, data)
        mock_socket.return_value.send.assert_called_once_with(expected_message)


if __name__ == '__main__':
    unittest.main()
