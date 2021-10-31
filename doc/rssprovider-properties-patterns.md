# Untitled array in RSS provider Schema

```txt
https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/patterns
```

list of regular expressions to match against the title of each RSS item. The corresponding URL will be passed to the downloader if any of these patterns match

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                    |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [RssProvider.json*](../out/providers/RssProvider.json "open original schema") |

## patterns Type

`string[]`
