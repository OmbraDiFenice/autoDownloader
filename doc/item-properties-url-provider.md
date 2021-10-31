# URL provider Schema

```txt
https://example.com/autoDownloader/schemas/items/Item.json#/properties/provider
```

Which method to use to get the download URL. Choose among the supported ones.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [Item.json*](../out/items/Item.json "open original schema") |

## provider Type

merged type ([URL provider](item-properties-url-provider.md))

one (and only one) of

*   [File provider](fileprovider.md "check type definition")

*   [HTML provider](htmlprovider.md "check type definition")

*   [RSS provider](rssprovider.md "check type definition")
