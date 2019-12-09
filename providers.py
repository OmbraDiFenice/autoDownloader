from abc import ABCMeta, abstractmethod
import requests
import xml.etree.ElementTree as ElementTree
import re
from validators import SpecValidatorMixin
from lxml.etree import HTMLParser
import lxml.etree
import logging


class AbstractProvider(SpecValidatorMixin, metaclass=ABCMeta):
    def __init__(self, spec, instance_class=None):
        self._validate_spec(spec, instance_class)

    @abstractmethod
    def get_urls(self):
        pass


class RssProvider(AbstractProvider):
    def __init__(self, spec, instance_class=None):
        super().__init__(spec, instance_class)
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
    def __init__(self, spec, instance_class=None):
        super().__init__(spec, instance_class)
        self.url = spec["url"]
        self.xpath = spec["xpath"]

    def _get_html_content(self):
        response = requests.get(self.url, verify=False)
        return response.text

    def _get_urls_using_xpath(self, html, xpath):
        root = self._parse_html(html)
        return root.xpath(xpath)

    @staticmethod
    def _parse_html(html):
        return lxml.etree.fromstring(html, parser=HTMLParser())

    def get_urls(self):
        html = self._get_html_content()
        urls = self._get_urls_using_xpath(html, self.xpath)
        return urls


class FileProvider(AbstractProvider):
    def __init__(self, spec, instance_class=None):
        super().__init__(spec, instance_class)
        self.path = spec["path"]

    def get_urls(self):
        with open(self.path, "r") as f:
            return [url.strip() for url in f.readlines()]


class LoggingHtmlProvider(HtmlProvider):
    def __init__(self, spec):
        super().__init__(spec, HtmlProvider)

    def _get_html_content(self):
        logging.info("fetching content from url {}".format(self.url))
        return super()._get_html_content()

    def _get_urls_using_xpath(self, html, xpath):
        urls = super()._get_urls_using_xpath(html, xpath)
        logging.info("found a total of {} urls".format(len(urls)))
        logging.debug(urls)
        return urls


class LoggingRssProvider(RssProvider):
    def __init__(self, spec):
        super().__init__(spec, RssProvider)

    def _get_xml(self):
        logging.info("fetching RSS xml from {}".format(self.url))
        return super()._get_xml()

    def _get_item_list(self, root):
        item_list = super()._get_item_list(root)
        logging.info("found a total of {} items".format(len(item_list)))
        return item_list

    def _filter_items_by_title(self, items):
        logging.info("filtering items on the title element according to {}".format(self.items_xpath))
        item_list = super()._filter_items_by_title(items)
        logging.info("{} items remaining".format(len(item_list)))
        logging.debug(item_list)
        return item_list

    def _get_url_list_from_item_list(self, items):
        url_list = super()._get_url_list_from_item_list(items)
        logging.debug("extracted url list: {}".format(url_list))
        return url_list
