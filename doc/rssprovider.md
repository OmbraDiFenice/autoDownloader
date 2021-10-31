# RSS provider Schema

```txt
https://example.com/autoDownloader/schemas/providers/RssProvider.json
```

Extracts links from an RSS feed. Can filter which RSS items to take into account using regular expressions on the title

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [RssProvider.json](../out/providers/RssProvider.json "open original schema") |

## RSS provider Type

`object` ([RSS provider](rssprovider.md))

# RSS provider Properties

| Property                  | Type     | Required | Nullable       | Defined by                                                                                                                                          |
| :------------------------ | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| [type](#type)             | `string` | Required | cannot be null | [RSS provider](rssprovider-properties-type.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/type")             |
| [url](#url)               | `string` | Required | cannot be null | [RSS provider](rssprovider-properties-url.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/url")               |
| [namespaces](#namespaces) | `object` | Optional | cannot be null | [RSS provider](rssprovider-properties-namespaces.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/namespaces") |
| [xpaths](#xpaths)         | `object` | Required | cannot be null | [RSS provider](rssprovider-properties-xpaths.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/xpaths")         |
| [patterns](#patterns)     | `array`  | Optional | cannot be null | [RSS provider](rssprovider-properties-patterns.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/patterns")     |

## type



`type`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [RSS provider](rssprovider-properties-type.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/type")

### type Type

`string`

### type Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value           | Explanation |
| :-------------- | :---------- |
| `"RssProvider"` |             |

## url

URL of the RSS feed. Should point to a standard RSS xml document

`url`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [RSS provider](rssprovider-properties-url.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/url")

### url Type

`string`

### url Constraints

**unknown format**: the value of this string must follow the format: `url`

## namespaces

mapping for the namespaces found in the RSS xml document. These are required for the XPath expression to work properly in case the elements mentioned in the expression are under a namespace

`namespaces`

*   is optional

*   Type: `object` ([Details](rssprovider-properties-namespaces.md))

*   cannot be null

*   defined in: [RSS provider](rssprovider-properties-namespaces.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/namespaces")

### namespaces Type

`object` ([Details](rssprovider-properties-namespaces.md))

## xpaths

XPath expressions used to identify, filter and extract the url from the RSS feed

`xpaths`

*   is required

*   Type: `object` ([Details](rssprovider-properties-xpaths.md))

*   cannot be null

*   defined in: [RSS provider](rssprovider-properties-xpaths.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/xpaths")

### xpaths Type

`object` ([Details](rssprovider-properties-xpaths.md))

## patterns

list of regular expressions to match against the title of each RSS item. The corresponding URL will be passed to the downloader if any of these patterns match

`patterns`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [RSS provider](rssprovider-properties-patterns.md "https://example.com/autoDownloader/schemas/providers/RssProvider.json#/properties/patterns")

### patterns Type

`string[]`
