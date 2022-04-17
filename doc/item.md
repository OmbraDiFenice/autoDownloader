# Download item Schema

```txt
https://example.com/autoDownloader/schemas/items/Item.json
```

Description of a download item and the options required to perform the download.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                 |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------- |
| Can be instantiated | Yes        | Unknown status | No           | Forbidden         | Allowed               | none                | [Item.json](../out/items/Item.json "open original schema") |

## Download item Type

`object` ([Download item](item.md))

# Download item Properties

| Property                                      | Type      | Required | Nullable       | Defined by                                                                                                                                |
| :-------------------------------------------- | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name)                                 | `string`  | Required | cannot be null | [Download item](item-properties-download-item-name.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/name")      |
| [enabled](#enabled)                           | `boolean` | Optional | cannot be null | [Download item](item-properties-item-is-enabled.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/enabled")      |
| [dest_dir](#dest_dir)                         | `string`  | Required | cannot be null | [Download item](item-properties-download-directory.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/dest_dir")  |
| [provider](#provider)                         | Merged    | Required | cannot be null | [Download item](item-properties-url-provider.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/provider")        |
| [cache](#cache)                               | Merged    | Optional | cannot be null | [Download item](item-properties-caching-method.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/cache")         |
| [downloader](#downloader)                     | Merged    | Required | cannot be null | [Download item](item-properties-download-method.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/downloader")   |
| [global_pre_script](#global_pre_script)       | Merged    | Optional | cannot be null | [Download item](item-definitions-script.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/global_pre_script")    |
| [global_post_script](#global_post_script)     | Merged    | Optional | cannot be null | [Download item](item-definitions-script.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/global_post_script")   |
| [pre_download_script](#pre_download_script)   | Merged    | Optional | cannot be null | [Download item](item-definitions-script.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/pre_download_script")  |
| [post_download_script](#post_download_script) | Merged    | Optional | cannot be null | [Download item](item-definitions-script.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/post_download_script") |

## name

User friendly name to refer to this download item.

`name`

*   is required

*   Type: `string` ([Download item name](item-properties-download-item-name.md))

*   cannot be null

*   defined in: [Download item](item-properties-download-item-name.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/name")

### name Type

`string` ([Download item name](item-properties-download-item-name.md))

## enabled

Set this to false to completely skip this item. It won't even run any pre/post script

`enabled`

*   is optional

*   Type: `boolean` ([Item is enabled](item-properties-item-is-enabled.md))

*   cannot be null

*   defined in: [Download item](item-properties-item-is-enabled.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/enabled")

### enabled Type

`boolean` ([Item is enabled](item-properties-item-is-enabled.md))

### enabled Default Value

The default value is:

```json
true
```

## dest_dir

Destination folder for the downloaded file.

`dest_dir`

*   is required

*   Type: `string` ([Download directory](item-properties-download-directory.md))

*   cannot be null

*   defined in: [Download item](item-properties-download-directory.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/dest_dir")

### dest_dir Type

`string` ([Download directory](item-properties-download-directory.md))

## provider

Which method to use to get the download URL. Choose among the supported ones.

`provider`

*   is required

*   Type: merged type ([URL provider](item-properties-url-provider.md))

*   cannot be null

*   defined in: [Download item](item-properties-url-provider.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/provider")

### provider Type

merged type ([URL provider](item-properties-url-provider.md))

one (and only one) of

*   [File provider](fileprovider.md "check type definition")

*   [HTML provider](htmlprovider.md "check type definition")

*   [RSS provider](rssprovider.md "check type definition")

## cache

As this script is meant to be run periodically, it can happen that the URL provider will return the same set of "available" URLs over and over. To avoid to trigger the download of the URLs that were already taken on the previous run a cache can be used. The downloader will skip any URL which is stored in the cache.

`cache`

*   is optional

*   Type: merged type ([Caching method](item-properties-caching-method.md))

*   cannot be null

*   defined in: [Download item](item-properties-caching-method.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/cache")

### cache Type

merged type ([Caching method](item-properties-caching-method.md))

one (and only one) of

*   [File cache](filecache.md "check type definition")

*   [Null cache](nullcache.md "check type definition")

## downloader

This is how you want to download each of the URLs returned by the Provider that needs downloading (i.e. that were not filtered by the cache).

`downloader`

*   is required

*   Type: merged type ([Download method](item-properties-download-method.md))

*   cannot be null

*   defined in: [Download item](item-properties-download-method.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/downloader")

### downloader Type

merged type ([Download method](item-properties-download-method.md))

one (and only one) of

*   [HTTP downloader](httpdownloader.md "check type definition")

*   [Torrent downloader](torrentdownloader.md "check type definition")

*   [Null downloader](nulldownloader.md "check type definition")

## global_pre_script

A script to be executed on certain events. Can be used to hook into the execution and perform extra computation on the downloaded files. It can be specified as a single string or as a list of strings. Refer to <https://docs.python.org/3.8/library/subprocess.html#subprocess.Popen>

`global_pre_script`

*   is optional

*   Type: merged type ([Script](item-definitions-script.md))

*   cannot be null

*   defined in: [Download item](item-definitions-script.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/global_pre_script")

### global_pre_script Type

merged type ([Script](item-definitions-script.md))

one (and only one) of

*   [Shell command](item-definitions-script-oneof-shell-command.md "check type definition")

*   [Executable](item-definitions-script-oneof-executable.md "check type definition")

## global_post_script

A script to be executed on certain events. Can be used to hook into the execution and perform extra computation on the downloaded files. It can be specified as a single string or as a list of strings. Refer to <https://docs.python.org/3.8/library/subprocess.html#subprocess.Popen>

`global_post_script`

*   is optional

*   Type: merged type ([Script](item-definitions-script.md))

*   cannot be null

*   defined in: [Download item](item-definitions-script.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/global_post_script")

### global_post_script Type

merged type ([Script](item-definitions-script.md))

one (and only one) of

*   [Shell command](item-definitions-script-oneof-shell-command.md "check type definition")

*   [Executable](item-definitions-script-oneof-executable.md "check type definition")

## pre_download_script

A script to be executed on certain events. Can be used to hook into the execution and perform extra computation on the downloaded files. It can be specified as a single string or as a list of strings. Refer to <https://docs.python.org/3.8/library/subprocess.html#subprocess.Popen>

`pre_download_script`

*   is optional

*   Type: merged type ([Script](item-definitions-script.md))

*   cannot be null

*   defined in: [Download item](item-definitions-script.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/pre_download_script")

### pre_download_script Type

merged type ([Script](item-definitions-script.md))

one (and only one) of

*   [Shell command](item-definitions-script-oneof-shell-command.md "check type definition")

*   [Executable](item-definitions-script-oneof-executable.md "check type definition")

## post_download_script

A script to be executed on certain events. Can be used to hook into the execution and perform extra computation on the downloaded files. It can be specified as a single string or as a list of strings. Refer to <https://docs.python.org/3.8/library/subprocess.html#subprocess.Popen>

`post_download_script`

*   is optional

*   Type: merged type ([Script](item-definitions-script.md))

*   cannot be null

*   defined in: [Download item](item-definitions-script.md "https://example.com/autoDownloader/schemas/items/Item.json#/properties/post_download_script")

### post_download_script Type

merged type ([Script](item-definitions-script.md))

one (and only one) of

*   [Shell command](item-definitions-script-oneof-shell-command.md "check type definition")

*   [Executable](item-definitions-script-oneof-executable.md "check type definition")

# Download item Definitions

## Definitions group script

Reference this group by using

```json
{"$ref":"https://example.com/autoDownloader/schemas/items/Item.json#/definitions/script"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |
