import subprocess
from factories import Factory
from validators import SpecValidatorMixin
import re
import os


class Item(SpecValidatorMixin):
    default_cache_spec = {
        "type": "NullCache"
    }

    def __init__(self, spec):
        self._validate_spec(spec)
        self.cache = self._init_cache(spec)
        self.provider = self._init_provider(spec)
        self.downloader = self._init_downloader(spec)
        self.dest_dir = spec.get("dest_dir", ".")
        self.global_pre_script = self._parse_script(spec.get("global_pre_script"))
        self.global_post_script = self._parse_script(spec.get("global_post_script"))
        self.pre_download_script = self._parse_script(spec.get("pre_download_script"))
        self.post_download_script = self._parse_script(spec.get("post_download_script"))

    @staticmethod
    def _parse_script(script):
        if script is not None and not isinstance(script, list):
            return re.split(r"\s+", script)
        return script

    @staticmethod
    def _init_downloader(spec):
        downloader_factory = Factory("downloaders")
        downloader_spec = spec["downloader"]
        return downloader_factory.create(downloader_spec)

    @staticmethod
    def _init_provider(spec):
        provider_factory = Factory("providers")
        provider_spec = spec["provider"]
        return provider_factory.create(provider_spec)

    def _init_cache(self, spec):
        cache_factory = Factory("caches")
        cache_spec = spec.get("cache", self.default_cache_spec)
        return cache_factory.create(cache_spec)

    def _filter_urls_in_cache(self, urls):
        return [url for url in urls if url not in self.cache]

    def download_new_elements(self):
        urls = self.provider.get_urls()
        urls_to_download = self._filter_urls_in_cache(urls)

        self._run_script(self.global_pre_script)
        for url in urls_to_download:
            self._run_script(self.pre_download_script, AUTODOWNLOADER_URL=url)
            file_name = self.downloader.download(url, self.dest_dir)
            self._run_script(self.post_download_script, AUTODOWNLOADER_URL=url, AUTODOWNLOADER_FILENAME=file_name)
            self.cache.store(url)
            self.cache.save()
        self._run_script(self.global_post_script)

    def _run_script(self, script, **extra_env):
        try:
            if script is None:
                return
            env = self._extend_environment(**extra_env)
            print("executing script: {}".format(" ".join(script)))
            subprocess.check_call(script, cwd=self.dest_dir, env=env)
        except subprocess.CalledProcessError as ex:
            print("Error during script: {}".format(script))
            print("return code is {}".format(ex.returncode))

    @staticmethod
    def _extend_environment(**extra_env):
        extended_env = os.environ.copy()
        extended_env.update(extra_env)
        return extended_env
