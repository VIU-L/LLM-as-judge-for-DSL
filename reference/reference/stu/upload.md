+++
title = "upload"
+++

## upload, tile type

The `upload` tile is intended to facilitate the upload of typically smaller files directly from an Envision dashboard, without navigating back and forth to the `Files` area in your Lokad account. When considering complex simulators that involve many parameters, it is often simpler to have all those parameters gathered in a spreadsheet, as opposed to entering all those values within a web page. While it is possible to upload such a spreadsheet like any other file in your Lokad account, it is more practical if the upload can happen directly within the dashboard. The `upload` tile is precisely intended to support this use case.

```envision
read upload "customsuppliers" as MySuppliers with
  SupplierId : text
  SupplierQuota : number
  SupplierCountry : text

show upload "Supplier settings" editable:"customsuppliers"
```

Unlike other tiles, the `upload` tile is tightly coupled with a corresponding `read upload` statement by means of a shared identifier (in the above example, `"customsuppliers"` is the shared identifier). Indeed, the syntax offers a way to treat the data uploaded by the user, just like any other table also accessible to Envision. The syntax lets you specify the expected format for the table columns to be uploaded within the dashboard. Also, just like any other data inputs, Envision provides a complete versioning of the uploaded files previously processed. The previously uploaded files can be re-downloaded from the _History_ link of the dashboard.

This _upload_ feature is accessible to any user who has access to the dashboard, without requiring the user to have access to the file storage area of your Lokad account. Thus the `upload` tile is also handy to provide more granular user accesses.
