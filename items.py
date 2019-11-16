from factories import Factory
from validators import SpecValidatorMixin


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
        for url in urls_to_download:
            self.downloader.download(url, self.dest_dir)
            self.cache.store(url)
        self.cache.save()
