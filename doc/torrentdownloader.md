# Torrent downloader Schema

```txt
https://example.com/autoDownloader/schemas/downloaders/TorrentDownloader.json
```

Sends the download information to a running rTorrent client. You need to setup rTorrent yourself. The actual download is entirely managed by rTorrent

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                 |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [TorrentDownloader.json](../out/downloaders/TorrentDownloader.json "open original schema") |

## Torrent downloader Type

`object` ([Torrent downloader](torrentdownloader.md))

# Torrent downloader Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                                                  |
| :------------ | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [type](#type) | `string` | Required | cannot be null | [Torrent downloader](torrentdownloader-properties-type.md "https://example.com/autoDownloader/schemas/downloaders/TorrentDownloader.json#/properties/type") |
| [host](#host) | `string` | Required | cannot be null | [Torrent downloader](torrentdownloader-properties-host.md "https://example.com/autoDownloader/schemas/downloaders/TorrentDownloader.json#/properties/host") |

## type



`type`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [Torrent downloader](torrentdownloader-properties-type.md "https://example.com/autoDownloader/schemas/downloaders/TorrentDownloader.json#/properties/type")

### type Type

`string`

### type Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value                 | Explanation |
| :-------------------- | :---------- |
| `"TorrentDownloader"` |             |

## host

Connection string to the rTorrent client. Can be the path to a Unix socket or an IP:port address, depending on how rTorrent is configured

`host`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [Torrent downloader](torrentdownloader-properties-host.md "https://example.com/autoDownloader/schemas/downloaders/TorrentDownloader.json#/properties/host")

### host Type

`string`
