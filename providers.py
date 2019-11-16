from abc import ABCMeta, abstractmethod
import requests
import xml.etree.ElementTree as ElementTree
import re
from validators import SpecValidatorMixin


class AbstractProvider(SpecValidatorMixin, metaclass=ABCMeta):
    def __init__(self, spec):
        self._validate_spec(spec)

    @abstractmethod
    def get_urls(self):
        pass


class RssProvider(AbstractProvider):
    def __init__(self, spec):
        super().__init__(spec)
        self.url = spec.get("url")
        self.namespaces = spec.get("namespaces", {})
        self.items_xpath = spec.get("xpaths", {}).get("items", "")
        self.url_xpath = spec.get("xpaths", {}).get("url", "")
        self.title_xpath = spec.get("xpaths", {}).get("title", "")
        self.patterns = spec.get("patterns", [".*"])
        if not self.patterns:
            self.patterns = [".*"]

    def _get_xml(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        response = requests.get(self.url, headers=headers)
        return response.text

    def _get_xml_root_node(self):
        xml = self._get_xml()
        return ElementTree.fromstring(xml)

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

    def _get_url_list_from_item_list(self, items):
        return [self._extract_url(item) for item in items]

    def get_urls(self):
        root = self._get_xml_root_node()
        result = self._get_item_list(root)
        result = self._filter_items_by_title(result)
        result = self._get_url_list_from_item_list(result)
        return result


class HtmlProvider(AbstractProvider):
    def __init__(self, spec):
        super().__init__(spec)
        pass

    def get_urls(self):
        pass
