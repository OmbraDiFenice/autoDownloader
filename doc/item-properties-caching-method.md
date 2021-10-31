# Caching method Schema

```txt
https://example.com/autoDownloader/schemas/items/Item.json#/properties/cache
```

As this script is meant to be run periodically, it can happen that the URL provider will return the same set of "available" URLs over and over. To avoid to trigger the download of the URLs that were already taken on the previous run a cache can be used. The downloader will skip any URL which is stored in the cache.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [Item.json*](../out/items/Item.json "open original schema") |

## cache Type

merged type ([Caching method](item-properties-caching-method.md))

one (and only one) of

*   [File cache](filecache.md "check type definition")

*   [Null cache](nullcache.md "check type definition")
