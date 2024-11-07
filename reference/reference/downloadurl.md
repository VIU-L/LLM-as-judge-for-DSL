+++
title = "downloadUrl"
+++

## downloadUrl(path: text) 🡒 text, pure function

Produces an [URL](../../stu/url/) that downloads the file at the specified [path](../../pqr/path/) in the Lokad file explorer.

Typical uses include: downloading data files, downloading PDF documents, or linking to images for display in `show label`.

```envision
show label (downloadUrl("/images/smiley.png")) 
```

If the user does not have permission to view the provided path, it is likely that they will not be able to download the file.

The file must be present in the Lokad file explorer at the time when the URL is visited, and it will always download the file present at that instant in time.

This function cannot be called on [try.lokad.com](https://try.lokad.com/).

## downloadUrl(hash: text, name: text) 🡒 text, pure function

Produces an [URL](../../stu/url/) that downloads the file with the specified hash, using the provided name.

Typical uses include: downloading data files, downloading PDF documents, or linking to images for display in `show label`.

```envision
show label (downloadUrl("4F7259333A6795C13F1AD9E900DAA7FE", "smiley.png")) 
```

Differences with the `downloadUrl(path)` version:

- The file can be downloaded even if the user does not have any permissions to access the Lokad file explorer.
- The file does not need to be present in the file explorer.
- The downloaded file is always the version with that specific hash, even if a new version is uploaded afterwards.

This function cannot be called on [try.lokad.com](https://try.lokad.com/).

## See also

- [fileUrl](../../def/fileurl/)
- [folderUrl](../../def/folderurl/)
- [previewUrl](../../pqr/previewurl/)
