# Main configuration Schema

```txt
https://example.com/autoDownloader/schemas/main.json
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                           |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [main.json](../out/main.json "open original schema") |

## Main configuration Type

`object` ([Main configuration](main.md))

## Main configuration Default Value

The default value is:

```json
{}
```

# Main configuration Properties

| Property        | Type    | Required | Nullable       | Defined by                                                                                                                            |
| :-------------- | :------ | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| [items](#items) | `array` | Required | cannot be null | [Main configuration](main-properties-download-items-list.md "https://example.com/autoDownloader/schemas/main.json#/properties/items") |

## items



`items`

*   is required

*   Type: `object[]` ([Download item](item.md))

*   cannot be null

*   defined in: [Main configuration](main-properties-download-items-list.md "https://example.com/autoDownloader/schemas/main.json#/properties/items")

### items Type

`object[]` ([Download item](item.md))

### items Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### items Default Value

The default value is:

```json
[]
```
