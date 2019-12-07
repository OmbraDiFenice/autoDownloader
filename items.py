import subprocess
from factories import Factory
from validators import SpecValidatorMixin
import re
import os
import logging


class Item(SpecValidatorMixin):
    default_cache_spec = {
        "type": "NullCache"
    }

    def __init__(self, spec, instance_class=None, downloader_factory=Factory("downloaders"), provider_factory=Factory("providers"), cache_factory=Factory("caches")):
        self.downloader_factory = downloader_factory
        self.provider_factory = provider_factory
        self.cache_factory = cache_factory
        self._validate_spec(spec, instance_class)
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

    def _init_downloader(self, spec):
        downloader_spec = spec["downloader"]
        return self.downloader_factory.create(downloader_spec)

    def _init_provider(self, spec):
        provider_spec = spec["provider"]
        return self.provider_factory.create(provider_spec)

    def _init_cache(self, spec):
        cache_spec = spec.get("cache", self.default_cache_spec)
        return self.cache_factory.create(cache_spec)

    def _filter_urls_in_cache(self, urls):
        return [url for url in urls if url not in self.cache]

    def get_urls_to_download(self):
        urls = self.provider.get_urls()
        return self._filter_urls_in_cache(urls)

    def download_new_elements(self):
        urls_to_download = self.get_urls_to_download()

        self._run_script(self.global_pre_script)
        for url in urls_to_download:
            self._run_script(self.pre_download_script, AUTODOWNLOADER_URL=url)
            file_name = self.downloader.download(url, self.dest_dir)
            self._run_script(self.post_download_script, AUTODOWNLOADER_URL=url, AUTODOWNLOADER_FILENAME=file_name)
            self.cache.store(url)
            self.cache.save()
        self._run_script(self.global_post_script)

    def _run_script(self, script, **extra_env):
        if script is None:
            return

        env = self._extend_environment(**extra_env)
        script_expanded = self._expand_variables(script, env)
        return subprocess.call(script_expanded, cwd=self.dest_dir, env=env)

    @staticmethod
    def _expand_variables(script, env):
        env_copy = os.environ.copy()
        os.environ.update(env)
        script_expanded = [os.path.expandvars(fragment) for fragment in script]
        os.environ = env_copy
        return script_expanded

    @staticmethod
    def _extend_environment(**extra_env):
        extended_env = os.environ.copy()
        extended_env.update(extra_env)
        return extended_env


class LoggingItem(Item):
    def __init__(self, spec):
        super().__init__(spec, Item)

    def _run_script(self, script, **extra_env):
        if script is None:
            return

        script_str = " ".join(script)
        logging.info("running script {}".format(script_str))
        return_code = super()._run_script(script, **extra_env)
        if return_code != 0:
            logging.warning("script {} failed, return code was: {}".format(script_str, return_code))
        else:
            logging.info("script {} terminated with return code 0".format(script_str, return_code))

    def _filter_urls_in_cache(self, urls):
        logging.debug("filtering urls excluding the cached ones...")
        urls = super()._filter_urls_in_cache(urls)
        if len(urls) == 0:
            logging.info("no new urls found: nothing to be done")
        else:
            logging.info("{} urls remaining after the filtering".format(len(urls)))
            logging.debug(urls)
        return urls
