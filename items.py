from factories import Factory


class Item:
    def __init__(self, config):
        self.cache = self._init_cache(config)
        self.provider = self._init_provider(config)
        self.downloader = self._init_downloader(config)
        self.dest_dir = config.get("dest_dir", ".")

    @staticmethod
    def _init_downloader(config):
        downloader_factory = Factory("downloaders")
        downloader_spec = config["downloader"]
        return downloader_factory.create(downloader_spec)

    @staticmethod
    def _init_provider(config):
        provider_factory = Factory("providers")
        provider_spec = config["provider"]
        return provider_factory.create(provider_spec)

    @staticmethod
    def _init_cache(config):
        cache_factory = Factory("caches")
        cache_spec = config["cache"]
        return cache_factory.create(cache_spec)
