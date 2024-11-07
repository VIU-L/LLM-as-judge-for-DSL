+++
title = "previewUrl"
+++

## previewUrl(hash: text, path: text) 🡒 text, pure function

Produces an [URL](../../stu/url/) that opens a preview page for the specified file.

The `hash` must correspond to a file that exists or has at point existed in the Lokad file storage.

The `path` argument is a [path](../pqr/path/) or a file name. It is included for informational purposes: the displayed contents are determined by the hash, not by the path. However, its extension must correspond to the actual file type (`.csv` for CSV files, `.ion` for Ionic files, and so on).

```envision
read "/sample/*.tsv" as _

show table "Loaded files" with
  Files.Path { href: #[ previewUrl(Files.Hash, Files.Path)] }
```

This function cannot be called on [try.lokad.com](https://try.lokad.com/).

## See also

- [downloadUrl](../../def/downloadurl/)
- [folderUrl](../../def/folderurl/)
- [fileUrl](../../pqr/fileurl/)
