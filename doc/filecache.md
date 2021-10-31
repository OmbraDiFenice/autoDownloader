# File cache Schema

```txt
https://example.com/autoDownloader/schemas/caches/FileCache.json
```

Caches URLs in a simple text file. Useful to easily tweak the content of the cache in case of errors or during the first test runs

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                            |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [FileCache.json](../out/caches/FileCache.json "open original schema") |

## File cache Type

`object` ([File cache](filecache.md))

# File cache Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                     |
| :------------ | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| [type](#type) | `string` | Required | cannot be null | [File cache](filecache-properties-type.md "https://example.com/autoDownloader/schemas/caches/FileCache.json#/properties/type") |
| [path](#path) | `string` | Required | cannot be null | [File cache](filecache-properties-path.md "https://example.com/autoDownloader/schemas/caches/FileCache.json#/properties/path") |

## type



`type`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [File cache](filecache-properties-type.md "https://example.com/autoDownloader/schemas/caches/FileCache.json#/properties/type")

### type Type

`string`

### type Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value         | Explanation |
| :------------ | :---------- |
| `"FileCache"` |             |

## path

Path to the file used to store the cached URLs

`path`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [File cache](filecache-properties-path.md "https://example.com/autoDownloader/schemas/caches/FileCache.json#/properties/path")

### path Type

`string`

### path Examples

```json
"cache/file/path"
```
