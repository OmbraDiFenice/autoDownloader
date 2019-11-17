from abc import ABCMeta, abstractmethod
from external_libraries.xmlrpc2scgi import do_scgi_xmlrpc_request as send_xmlrpc
from validators import SpecValidatorMixin
import re
import os
import requests


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


class HttpDownloader(AbstractDownloader):
    def __init__(self, spec):
        super().__init__(spec)

    def _get_file_name(self, response):
        content_disposition = response.headers.get("content-disposition", "")
        match = re.findall(r"filename=([^\s])", content_disposition)
        if not match:
            return "temp_filename"
        return match[0]

    def download(self, url, dest_dir):
        response = requests.get(url)
        filename = self._get_file_name(response)
        with open(os.path.join(dest_dir, filename), "wb") as f:
            f.write(response.content)
