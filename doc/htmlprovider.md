# HTML provider Schema

```txt
https://example.com/autoDownloader/schemas/providers/HtmlProvider.json
```

Extract URLs from a given HTML web page using an XPath expression to find the link. Uses lxml for non-well formed HTML documents.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                     |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [HtmlProvider.json](../out/providers/HtmlProvider.json "open original schema") |

## HTML provider Type

`object` ([HTML provider](htmlprovider.md))

# HTML provider Properties

| Property        | Type     | Required | Nullable       | Defined by                                                                                                                                   |
| :-------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
| [type](#type)   | `string` | Required | cannot be null | [HTML provider](htmlprovider-properties-type.md "https://example.com/autoDownloader/schemas/providers/HtmlProvider.json#/properties/type")   |
| [url](#url)     | `string` | Required | cannot be null | [HTML provider](htmlprovider-properties-url.md "https://example.com/autoDownloader/schemas/providers/HtmlProvider.json#/properties/url")     |
| [xpath](#xpath) | `string` | Required | cannot be null | [HTML provider](htmlprovider-properties-xpath.md "https://example.com/autoDownloader/schemas/providers/HtmlProvider.json#/properties/xpath") |

## type



`type`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [HTML provider](htmlprovider-properties-type.md "https://example.com/autoDownloader/schemas/providers/HtmlProvider.json#/properties/type")

### type Type

`string`

### type Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value            | Explanation |
| :--------------- | :---------- |
| `"HtmlProvider"` |             |

## url

URL of the web page containing the links to extract

`url`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [HTML provider](htmlprovider-properties-url.md "https://example.com/autoDownloader/schemas/providers/HtmlProvider.json#/properties/url")

### url Type

`string`

### url Constraints

**unknown format**: the value of this string must follow the format: `url`

## xpath

XPath expression inside the HTML document pointed by the url parameter. Should return a link usable by the downloader later on

`xpath`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [HTML provider](htmlprovider-properties-xpath.md "https://example.com/autoDownloader/schemas/providers/HtmlProvider.json#/properties/xpath")

### xpath Type

`string`
