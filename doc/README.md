# README

## Top-level Schemas

*   [Download item](./item.md "Description of a download item and the options required to perform the download") – `https://example.com/autoDownloader/schemas/items/Item.json`

*   [File cache](./filecache.md "Caches URLs in a simple text file") – `https://example.com/autoDownloader/schemas/caches/FileCache.json`

*   [File provider](./fileprovider.md "Read URLs from a text file, one per line") – `https://example.com/autoDownloader/schemas/providers/FileProvider.json`

*   [HTML provider](./htmlprovider.md "Extract URLs from a given HTML web page using an XPath expression to find the link") – `https://example.com/autoDownloader/schemas/providers/HtmlProvider.json`

*   [HTTP downloader](./httpdownloader.md "Download URLs via a simple HTTP direct connection") – `https://example.com/autoDownloader/schemas/downloaders/HttpDownloader.json`

*   [Main configuration](./main.md) – `https://example.com/autoDownloader/schemas/main.json`

*   [Null cache](./nullcache.md "Fake cache that doesn't cache anything") – `https://example.com/autoDownloader/schemas/caches/NullCache.json`

*   [Null downloader](./nulldownloader.md "Fake downloader that doesn't do anything") – `https://example.com/autoDownloader/schemas/downloaders/NullDownloader.json`

*   [RSS provider](./rssprovider.md "Extracts links from an RSS feed") – `https://example.com/autoDownloader/schemas/providers/RssProvider.json`

*   [Torrent downloader](./torrentdownloader.md "Sends the download information to a running rTorrent client") – `https://example.com/autoDownloader/schemas/downloaders/TorrentDownloader.json`

## Other Schemas

### Objects

*   [Untitled object in RSS provider](./rssprovider-properties-namespaces.md "mapping for the namespaces found in the RSS xml document") – `https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/namespaces`

*   [Untitled object in RSS provider](./rssprovider-properties-xpaths.md "XPath expressions used to identify, filter and extract the url from the RSS feed") – `https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/xpaths`

*   [Untitled object in RSS provider](./rssprovider-properties-namespaces.md "mapping for the namespaces found in the RSS xml document") – `https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/namespaces`

*   [Untitled object in RSS provider](./rssprovider-properties-xpaths.md "XPath expressions used to identify, filter and extract the url from the RSS feed") – `https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/xpaths`

### Arrays

*   [Download items list](./main-properties-download-items-list.md) – `https://example.com/autoDownloader/schemas/main.json#/properties/items`

*   [Executable](./item-definitions-script-oneof-executable.md "A list of strings where the first one indicates the absolute path to the program and the remaining are the parameters passed to it") – `https://example.com/autoDownloader/schemas/items/Item.json#/definitions/script/oneOf/1`

*   [Executable](./item-definitions-script-oneof-executable.md "A list of strings where the first one indicates the absolute path to the program and the remaining are the parameters passed to it") – `https://example.com/autoDownloader/schemas/items/Item.json#/definitions/script/oneOf/1`

*   [Executable](./item-definitions-script-oneof-executable.md "A list of strings where the first one indicates the absolute path to the program and the remaining are the parameters passed to it") – `https://example.com/autoDownloader/schemas/items/Item.json#/definitions/script/oneOf/1`

*   [Executable](./item-definitions-script-oneof-executable.md "A list of strings where the first one indicates the absolute path to the program and the remaining are the parameters passed to it") – `https://example.com/autoDownloader/schemas/items/Item.json#/definitions/script/oneOf/1`

*   [Executable](./item-definitions-script-oneof-executable.md "A list of strings where the first one indicates the absolute path to the program and the remaining are the parameters passed to it") – `https://example.com/autoDownloader/schemas/items/Item.json#/definitions/script/oneOf/1`

*   [Executable](./item-definitions-script-oneof-executable.md "A list of strings where the first one indicates the absolute path to the program and the remaining are the parameters passed to it") – `https://example.com/autoDownloader/schemas/items/Item.json#/definitions/script/oneOf/1`

*   [Executable](./item-definitions-script-oneof-executable.md "A list of strings where the first one indicates the absolute path to the program and the remaining are the parameters passed to it") – `https://example.com/autoDownloader/schemas/items/Item.json#/definitions/script/oneOf/1`

*   [Executable](./item-definitions-script-oneof-executable.md "A list of strings where the first one indicates the absolute path to the program and the remaining are the parameters passed to it") – `https://example.com/autoDownloader/schemas/items/Item.json#/definitions/script/oneOf/1`

*   [Executable](./item-definitions-script-oneof-executable.md "A list of strings where the first one indicates the absolute path to the program and the remaining are the parameters passed to it") – `https://example.com/autoDownloader/schemas/items/Item.json#/definitions/script/oneOf/1`

*   [Executable](./item-definitions-script-oneof-executable.md "A list of strings where the first one indicates the absolute path to the program and the remaining are the parameters passed to it") – `https://example.com/autoDownloader/schemas/items/Item.json#/definitions/script/oneOf/1`

*   [Untitled array in RSS provider](./rssprovider-properties-patterns.md "list of regular expressions to match against the title of each RSS item") – `https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/patterns`

*   [Untitled array in RSS provider](./rssprovider-properties-patterns.md "list of regular expressions to match against the title of each RSS item") – `https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/patterns`

## Version Note

The schemas linked above follow the JSON Schema Spec version: `http://json-schema.org/draft-07/schema#`
