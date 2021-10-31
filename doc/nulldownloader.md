# Null downloader Schema

```txt
https://example.com/autoDownloader/schemas/downloaders/NullDownloader.json
```

Fake downloader that doesn't do anything. Useful in case you're defining an item just to fetch URLs that are then handled via external scripts

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                           |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [NullDownloader.json](../out/downloaders/NullDownloader.json "open original schema") |

## Null downloader Type

`object` ([Null downloader](nulldownloader.md))

# Null downloader Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                                         |
| :------------ | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| [type](#type) | `string` | Required | cannot be null | [Null downloader](nulldownloader-properties-type.md "https://example.com/autoDownloader/schemas/downloaders/NullDownloader.json#/properties/type") |

## type



`type`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [Null downloader](nulldownloader-properties-type.md "https://example.com/autoDownloader/schemas/downloaders/NullDownloader.json#/properties/type")

### type Type

`string`

### type Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value              | Explanation |
| :----------------- | :---------- |
| `"NullDownloader"` |             |
