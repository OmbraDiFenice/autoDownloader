from abc import ABCMeta, abstractmethod
from external_libraries.xmlrpc2scgi import do_scgi_xmlrpc_request as send_xmlrpc


class AbstractDownloader(metaclass=ABCMeta):
    @abstractmethod
    def download(self, url, dest_dir):
        pass


class TorrentDownloader(AbstractDownloader):
    def __init__(self, host):
        self.host = host

    def download(self, url, dest_dir):
        method = "load.start"
        params = ("", url, "d.directory.set={}".format(dest_dir))
        send_xmlrpc(self.host, method, params)
