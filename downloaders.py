from abc import ABCMeta, abstractmethod
from external_libraries.xmlrpc2scgi import do_scgi_xmlrpc_request as send_xmlrpc
from validators import SpecValidatorMixin
import re
import os
import requests
import logging


class AbstractDownloader(SpecValidatorMixin, metaclass=ABCMeta):
    def __init__(self, spec, instance_class=None):
        self._validate_spec(spec, instance_class)

    @abstractmethod
    def download(self, url, dest_dir, skip=False):
        pass


class NullDownloader(AbstractDownloader):
    def __init__(self, spec, instance_class=None):
        super().__init__(spec, instance_class)

    def download(self, url, dest_dir, skip=False):
        return "fakeFile"


class TorrentDownloader(AbstractDownloader):
    def __init__(self, spec, instance_class=None):
        super().__init__(spec, instance_class)
        self.host = spec["host"]

    def download(self, url, dest_dir, skip=False):
        method = "load.start"
        params = ("", url, 'd.directory.set="{}"'.format(dest_dir))
        if not skip:
            self._start_torrent(method, params)
        return self._get_torrent_name(url)

    @staticmethod
    def _get_torrent_name(url):
        return url.split("/")[-1]

    def _start_torrent(self, method, params):
        send_xmlrpc(self.host, method, params)


class HttpDownloader(AbstractDownloader):
    def __init__(self, spec, instance_class=None):
        super().__init__(spec, instance_class)
        self.method = spec["method"].upper()

    @staticmethod
    def _extract_filename_from_request(request):
        url = request.path_url
        return url.split("/")[-1]

    def _get_file_name(self, response):
        content_disposition = response.headers.get("content-disposition", "")
        match = re.findall(r"filename=[\"']?([^\"']+)[\"']?", content_disposition)
        if not match:
            return self._extract_filename_from_request(response.request)
        return match[0]

    def _download(self, url):
        common_options = {
            "verify": False
        }
        if self.method == "GET":
            return requests.get(url, **common_options, stream=True)
        elif self.method == "POST":
            return requests.post(url, **common_options, stream=True)
        else:
            raise Exception("Invalid method: %s", self.method)

    def download(self, url, dest_dir, skip=False):
        if not skip:
            response = self._download(url)
            filename = self._get_file_name(response)
            with open(os.path.join(dest_dir, filename), "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                response.close()
            return filename
        return "download skipped, no filename available"


class LoggingHttpDownloader(HttpDownloader):
    def __init__(self, spec):
        super().__init__(spec, HttpDownloader)

    def download(self, url, dest_dir, skip=False):
        logging.info("starting download of {}, dest folder: {}".format(url, dest_dir))
        file_name = super().download(url, dest_dir, skip)
        logging.info("download terminated, file saved as {}".format(file_name))
        return file_name


class LoggingTorrentDownloader(TorrentDownloader):
    def __init__(self, spec):
        super().__init__(spec, TorrentDownloader)

    def _start_torrent(self, method, params):
        logging.debug("enqueuing torrent; method: {}, params: {}".format(method, params))
        return super()._start_torrent(method, params)

    def download(self, url, dest_dir, skip=False):
        logging.info("starting download of {}, setting dest_dir to {}".format(url, dest_dir))
        return super().download(url, dest_dir, skip)
