# Download method Schema

```txt
https://example.com/autoDownloader/schemas/items/Item.json#/properties/downloader
```

This is how you want to download each of the URLs returned by the Provider that needs downloading (i.e. that were not filtered by the cache).

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [Item.json*](../out/items/Item.json "open original schema") |

## downloader Type

merged type ([Download method](item-properties-download-method.md))

one (and only one) of

*   [HTTP downloader](httpdownloader.md "check type definition")

*   [Torrent downloader](torrentdownloader.md "check type definition")

*   [Null downloader](nulldownloader.md "check type definition")
