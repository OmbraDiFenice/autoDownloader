# Configurable downloader script

Check different data sources for content and trigger the download of new elements.

This script is designed to be run periodically (e.g. with a cronjob) to regularly check and automatically download
new content when it comes out.

I wrote this as a kind of exercise to experiment with some design patterns in Python.
There is no particular focus about performances or reliability (at least not yet).

# Disclaimer

This script only triggers the download of given URLs. I'm not responsible for the usage you do with this software,
for any damage might result by using it, and I'm certainly not encouraging piracy in any form.

## Main features

 - Handle different types of data sources as well as perform the downloads in different ways
 - An optional caching system ensures that the same content is not downloaded multiple times
 - Easy to add support for new methods of fetch, download and cache URLs
 - Pre/Post download hooks for quick tweaking/extension of default behavior via scripts

# Requisites

 - Python >= 3.8

# Usage

 1. clone the repo
 2. install dependencies: `cd autoDownloader && pip install -r requirements.txt`
 3. create a `config.json` file in the main repo folder (see example below)
 4. Check `python main.py -h` for the available command line options
 5. try it out: `python main.py`. The command itself won't output anything, but you can follow the execution by checking the log with `tail -f autoDownloader.log` in another shell.
 6. once you verified that everything works fine, schedule a periodic execution, e.g. every day at 01:00AM

Example of `config.json` file:
```json
{
  "items": [
    {
      "name": "My favorite content",
      "dest_dir": "/home/user/downloads/auto_downloads",
      "provider": {
        "type": "RssProvider",
        "url": "https://example-rss.com/rss.xml",
        "namespaces": {
          "ns0": "https://example-rss.com"
        },
        "xpaths": {
          "title": "/title",
          "items": "//item",
          "url": "/link"
        },
        "patterns": [
          "filtering-regexp"
        ]
      },
      "cache": {
        "type": "FileCache",
        "path": "/home/user/downloads/auto_downloads/cache.txt"
      },
      "downloader": {
        "type": "HttpDownloader",
        "method": "GET"
      },
      "global_pre_script": "/home/user/downloads/auto_downloads/pre_script.sh",
      "post_downloads_script": "/home/user/downloads/auto_downloads/post_download.sh"
    }
  ]
}
```

# Quick guide

## Items

Items describe your download definitions. Each item contains the configuration
telling the script how to check and download content from a specific source.

The main configuration contains a list of item definitions, which are executed in order.
The ordering can be important if you want to use scripts to build a complex download mechanism for a certain data source.

Each item contains at least a `name`, a `destination folder` and one of each:
 - `provider`
 - `cache`
 - `downloader`

Check the [reference](doc/item.md) for the complete list of fields.

The supported providers, caches and downloaders can be easily extended in the code;
take a look at the existing ones for reference.

### Scripts

You can specify some script to be run on certain hooks. Currently the available hooks are:

#### global_pre_script

Executed before the download of any URL from the current item has started

#### global_post_script

Executed after the download of all the URLs from the current item has finished

#### pre_download_script

Executed before the download of each URL from the current item.

Available environment variables:
 - AUTODOWNLOADER_URL: URL about to be downloaded

#### post_download_script

Executed after the download of each URL from the current item.

Available environment variables:
 - AUTODOWNLOADER_URL: URL of the downloaded content
 - AUTODOWNLOADER_FILENAME: destination file name

## Providers

The provider description in each item defines how to fetch information about the content to download.
Ultimately this results in a list of URLs, which will get passed to the cache and finally to the downloader.

### Supported URL providers

 - [RSS feeds](doc/rssprovider.md)
 - [HTML web pages](doc/htmlprovider.md)
 - [Text file](doc/fileprovider.md)

## Caches

As this script is meant to be run periodically, it can happen that the URL provider will return the same set
of available URLs over and over.

To avoid triggering the download of the URLs that were already taken on the
previous run a cache can be used. The downloader will skip any URL which is stored in the cache.

### Supported caches

 - [On file](doc/filecache.md)
 - [NullCache](doc/nullcache.md) (just skip caching)

## Downloaders

The downloader is the component that is effectively taking care of downloading the content from a URL.

### Supported download methods

 - [Direct download over HTTP](doc/httpdownloader.md)
 - [Torrent](doc/torrentdownloader.md) (via [rTorrent client](https://github.com/rakshasa/rtorrent))
 - [NullDownloader](doc/nulldownloader.md) (skip download)

# Development

## Testing

**Please add new tests if you want to add new functionalities or fix bugs.**

The code is unit tested with [unittest](https://docs.python.org/3.8/library/unittest.html) module, so no extra libraries
are needed to run them. Just make sure that the repo root is in your PYTHONPATH and then run

```sh
python -m unittest
```

Note that python 3.8 or higher is required to run the tests.

## Documentation

The configuration file format is defined with [jsonschema](https://json-schema.org/). The definition files are under the `schemas` folder.

The jsonschema configuration is checked at runtime when the config is loaded, so the definitions _must_ be updated in case of extension.

To generate the markdown description out of the jsonschema definitions use [jsonschema2md](https://github.com/adobe/jsonschema2md) with the following options:

```sh
jsonschema2md -d schemas -e json -o doc
```