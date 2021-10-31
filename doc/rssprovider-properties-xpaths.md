# Untitled object in RSS provider Schema

```txt
https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/xpaths
```

XPath expressions used to identify, filter and extract the url from the RSS feed

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                    |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [RssProvider.json*](../out/providers/RssProvider.json "open original schema") |

## xpaths Type

`object` ([Details](rssprovider-properties-xpaths.md))

# xpaths Properties

| Property        | Type     | Required | Nullable       | Defined by                                                                                                                                                                    |
| :-------------- | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [items](#items) | `string` | Required | cannot be null | [RSS provider](rssprovider-properties-xpaths-properties-items.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/xpaths/properties/items") |
| [url](#url)     | `string` | Required | cannot be null | [RSS provider](rssprovider-properties-xpaths-properties-url.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/xpaths/properties/url")     |
| [title](#title) | `string` | Required | cannot be null | [RSS provider](rssprovider-properties-xpaths-properties-title.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/xpaths/properties/title") |

## items

XPath locating all the items in the feed. The expression starts at the root of the RSS document

`items`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [RSS provider](rssprovider-properties-xpaths-properties-items.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/xpaths/properties/items")

### items Type

`string`

### items Examples

```json
"//item"
```

## url

XPath locating the download URL inside each item. The path starts with the item at its root, as returned by the "items" XPath

`url`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [RSS provider](rssprovider-properties-xpaths-properties-url.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/xpaths/properties/url")

### url Type

`string`

### url Examples

```json
"/link"
```

## title

XPath locating the title inside each item. The path starts with the item at its root, as returned by the "items" XPath

`title`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [RSS provider](rssprovider-properties-xpaths-properties-title.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/xpaths/properties/title")

### title Type

`string`

### title Examples

```json
"/title"
```
