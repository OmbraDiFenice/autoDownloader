# File provider Schema

```txt
https://example.com/autoDownloader/schemas/providers/FileProvider.json
```

Read URLs from a text file, one per line. The file is not emptied, so on the next run the same URLs will be returned.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                     |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [FileProvider.json](../out/providers/FileProvider.json "open original schema") |

## File provider Type

`object` ([File provider](fileprovider.md))

# File provider Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                                 |
| :------------ | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| [type](#type) | `string` | Required | cannot be null | [File provider](fileprovider-properties-type.md "https://example.com/autoDownloader/schemas/providers/FileProvider.json#/properties/type") |
| [path](#path) | `string` | Required | cannot be null | [File provider](fileprovider-properties-path.md "https://example.com/autoDownloader/schemas/providers/FileProvider.json#/properties/path") |

## type



`type`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [File provider](fileprovider-properties-type.md "https://example.com/autoDownloader/schemas/providers/FileProvider.json#/properties/type")

### type Type

`string`

### type Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value            | Explanation |
| :--------------- | :---------- |
| `"FileProvider"` |             |

## path

Path to the file containing the URLs

`path`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [File provider](fileprovider-properties-path.md "https://example.com/autoDownloader/schemas/providers/FileProvider.json#/properties/path")

### path Type

`string`
