# Untitled string in RSS provider Schema

```txt
https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/xpaths/properties/items
```

XPath locating all the items in the feed. The expression starts at the root of the RSS document

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                    |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [RssProvider.json*](../out/providers/RssProvider.json "open original schema") |

## items Type

`string`

## items Examples

```json
"//item"
```
