# Download items list Schema

```txt
https://example.com/autoDownloader/schemas/main.json#/properties/items
```



| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                            |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [main.json*](../out/main.json "open original schema") |

## items Type

`object[]` ([Download item](item.md))

## items Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## items Default Value

The default value is:

```json
[]
```
