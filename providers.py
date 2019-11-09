import requests
import xml.etree.ElementTree as ET
import re
from caches import NullCache


class RssProvider:
    def __init__(self, spec, cache=NullCache()):
        self.url = spec.get("url")
        self.namespaces = spec.get("namespaces", {})
        self.items_xpath = spec.get("xpaths", {}).get("items", "")
        self.url_xpath = spec.get("xpaths", {}).get("url", "")
        self.title_xpath = spec.get("xpaths", {}).get("title", "")
        self.patterns = spec.get("patterns", [".*"])
        self.dest_dir = spec.get("dest_dir", ".")

        self.cache = cache

    def _get_xml(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        response = requests.get(self.url, headers=headers)
        return response.text

    def _get_xml_root_node(self):
        xml = self._get_xml()
        return ET.fromstring(xml)

    def _match_xpath(self, root, xpath):
        xpath = xpath if xpath.startswith(".") else "." + xpath
        m = re.search("(.+)/@(.\\w+)$", xpath)
        attr = None
        if m:
            attr = m.group(2)
            xpath = m.group(1)
        found = root.findall(xpath, self.namespaces)
        if len(found) == 1:
            if attr is not None:
                return found[0].attrib[attr]
            else:
                return found[0].text
        return found

    def _get_item_list(self, root):
        return self._match_xpath(root, self.items_xpath)

    def _extract_url(self, item):
        return self._match_xpath(item, self.url_xpath)

    def _match_item_title(self, item):
        title = self._match_xpath(item, self.title_xpath)
        return any([re.search(regex, title) for regex in self.patterns])

    def _filter_items_by_title(self, items):
        return [item for item in items if self._match_item_title(item)]

    def _filter_urls_in_cache(self, items):
        return [item for item in items if item not in self.cache]

    def _get_url_list_from_item_list(self, items):
        return [self._extract_url(item) for item in items]

    def get_urls(self):
        root = self._get_xml_root_node()
        result = self._get_item_list(root)
        result = self._filter_items_by_title(result)
        result = self._get_url_list_from_item_list(result)
        result = self._filter_urls_in_cache(result)
        return result


class HtmlProvider:
    pass


def create_provider(specs, cache=NullCache()):
    if "type" not in specs.keys():
        raise ProviderFactoryError("Unable to create provider: type not defined")
    if specs.get("type") == "rss":
        return RssProvider(specs, cache=cache)
    if specs.get("type") == "html":
        return HtmlProvider()
    raise ProviderFactoryError("Unable to create provider: type '{}' not known".format(specs.get("type")))


class ProviderFactoryError(Exception):
    pass
