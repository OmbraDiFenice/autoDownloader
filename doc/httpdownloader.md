# HTTP downloader Schema

```txt
https://example.com/autoDownloader/schemas/downloaders/HttpDownloader.json
```

Download URLs via a simple HTTP direct connection.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                           |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [HttpDownloader.json](../out/downloaders/HttpDownloader.json "open original schema") |

## HTTP downloader Type

`object` ([HTTP downloader](httpdownloader.md))

# HTTP downloader Properties

| Property          | Type     | Required | Nullable       | Defined by                                                                                                                                             |
| :---------------- | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| [type](#type)     | `string` | Required | cannot be null | [HTTP downloader](httpdownloader-properties-type.md "https://example.com/autoDownloader/schemas/downloaders/HttpDownloader.json#/properties/type")     |
| [method](#method) | `string` | Required | cannot be null | [HTTP downloader](httpdownloader-properties-method.md "https://example.com/autoDownloader/schemas/downloaders/HttpDownloader.json#/properties/method") |

## type



`type`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [HTTP downloader](httpdownloader-properties-type.md "https://example.com/autoDownloader/schemas/downloaders/HttpDownloader.json#/properties/type")

### type Type

`string`

### type Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value              | Explanation |
| :----------------- | :---------- |
| `"HttpDownloader"` |             |

## method

The HTTP verb to use for download

`method`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [HTTP downloader](httpdownloader-properties-method.md "https://example.com/autoDownloader/schemas/downloaders/HttpDownloader.json#/properties/method")

### method Type

`string`

### method Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value    | Explanation |
| :------- | :---------- |
| `"POST"` |             |
| `"GET"`  |             |
