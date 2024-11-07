+++
title = "folderUrl"
+++

## folderUrl(path: text) 🡒 text, pure function

Produces an [URL](../../stu/url/) that opens the Lokad file explorer on the folder at the specified [path](../../pqr/path/).

```envision
show menu "Data folders" with
  "Input"  { href: #[folderUrl("/input")] }
  "Output" { href: #[folderUrl("/output")] }
```

End users will usually not be granted access to see the Lokad file explorer, so this function is mostly intended to design tools for internal use.

This function cannot be called on [try.lokad.com](https://try.lokad.com/).

## See also

- [downloadUrl](../../def/downloadurl/)
- [fileUrl](../../def/fileurl/)
- [previewUrl](../../pqr/previewurl/)
