from abc import ABCMeta, abstractmethod
from external_libraries.xmlrpc2scgi import do_scgi_xmlrpc_request as send_xmlrpc
from validators import SpecValidatorMixin


class AbstractDownloader(SpecValidatorMixin, metaclass=ABCMeta):
    def __init__(self, spec):
        self._validate_spec(spec)

    @abstractmethod
    def download(self, url, dest_dir):
        pass


class TorrentDownloader(AbstractDownloader):
    def __init__(self, spec):
        super().__init__(spec)
        self.host = spec["host"]

    def download(self, url, dest_dir):
        method = "load.start"
        params = ("", url, "d.directory.set={}".format(dest_dir))
        send_xmlrpc(self.host, method, params)
