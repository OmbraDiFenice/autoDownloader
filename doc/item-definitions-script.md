# Script Schema

```txt
https://example.com/autoDownloader/schemas/items/Item.json#/definitions/script
```

A script to be executed on certain events. Can be used to hook into the execution and perform extra computation on the downloaded files. It can be specified as a single string or as a list of strings. Refer to <https://docs.python.org/3.8/library/subprocess.html#subprocess.Popen>

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [Item.json*](../out/items/Item.json "open original schema") |

## script Type

merged type ([Script](item-definitions-script.md))

one (and only one) of

*   [Shell command](item-definitions-script-oneof-shell-command.md "check type definition")

*   [Executable](item-definitions-script-oneof-executable.md "check type definition")
