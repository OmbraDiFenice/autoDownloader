# Null cache Schema

```txt
https://example.com/autoDownloader/schemas/caches/NullCache.json
```

Fake cache that doesn't cache anything. Use if you don't need caching.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                            |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [NullCache.json](../out/caches/NullCache.json "open original schema") |

## Null cache Type

`object` ([Null cache](nullcache.md))

# Null cache Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                     |
| :------------ | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| [type](#type) | `string` | Required | cannot be null | [Null cache](nullcache-properties-type.md "https://example.com/autoDownloader/schemas/caches/NullCache.json#/properties/type") |

## type



`type`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [Null cache](nullcache-properties-type.md "https://example.com/autoDownloader/schemas/caches/NullCache.json#/properties/type")

### type Type

`string`

### type Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value         | Explanation |
| :------------ | :---------- |
| `"NullCache"` |             |
