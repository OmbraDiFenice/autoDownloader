class Provider:
    pass


class RssProvider(Provider):
    pass


class HtmlProvider(Provider):
    pass


def create_provider(specs):
    if "type" not in specs.keys():
        raise ProviderFactoryError("Unable to create provider: type not defined")
    if specs.get("type") == "rss":
        return RssProvider()
    if specs.get("type") == "html":
        return HtmlProvider()
    raise ProviderFactoryError("Unable to create provider: type '{}' not known".format(specs.get("type")))


class ProviderFactoryError(Exception):
    pass
