+++
title = "fileUrl"
+++

## fileUrl(path: text) 🡒 text, pure function

Produces an [URL](../../stu/url/) that opens the Lokad file explorer on the folder that contains the file at the specified [path](../../pqr/path/), and highlights the file if it exists.

```envision
read "/sample/*.tsv" as _

show table "Loaded files" with
  Files.Path { href: #[fileUrl(Files.Path)] }
```

End users will usually not be granted access to see the Lokad file explorer, so this function is mostly intended to design tools for internal use.

This function cannot be called on [try.lokad.com](https://try.lokad.com/).

## See also

- [downloadUrl](../../def/downloadurl/)
- [folderUrl](../../def/folderurl/)
- [previewUrl](../../pqr/previewurl/)
