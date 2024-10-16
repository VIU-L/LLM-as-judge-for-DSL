+++
title = "Writing files"
description = ""
weight = 1
+++

Files are written either to be consumed by later scripts, or to be exported to third-party systems outside Lokad.

**Table of contents**
{{< toc >}}{{< /toc >}}

## The `write` statement

Writing a file in Envision is expected to be done through a `write` statement:

```envision
table Products = with
  [| as Product, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]

write Products as "/sample/products.csv" with
  Product = Products.Product
  Color = Products.Color
  Price = if Products.Price > 0 then Products.Price else 100
```

**Roadmap:** Most of the formatting capabilities of the `write` option (detailed below) have not yet been ported to the `write` statement. All those capabilities will gradually be made available for `write` statements.

## The `write` option

Writing files in Envision can also be done through the `table` tile and the `write` option. The `table` tile is the only tile that allows its content to be persisted as a file. Let’s revisit one script that we introduced previously:

```envision
table Products = with
  [| as Product, as Price |]
  [| "shirt", 10.50 |]
  [| "pants", 15.00 |]
  [| "hat", 5.25 |]

table Goods = with
  [| as Good, as Price |]
  [| "t-shirt", 4.25 |]
  [| "bandana", 3.75 |]

show table "Products" a1b3 write:"/sample/products.csv" with
  Products.Product
  Products.Price

show table "Products" c1d3 write:"/sample/goods.csv" with
  Goods.Good
  Goods.Price
```

The above script results in the production of the two files `products.csv` and `goods.csv`. The `write` option must be positioned after the tile title and after the tile position (if present).

In Envision, file writes are _atomic_. From the perspective of all the other Envision scripts, and even from the perspective of SFTP/FTPS clients, the output files are absent until they are present _in their final form_. The Lokad platform prevents any third party from accessing the files while writing is in progress.

It is possible to control the export’s file format by picking the right file name extension. For example, a Microsoft Excel spreadsheet can be produced with:

```envision
table Products = with
  [| as Product, as Price |]
  [| "shirt", 10.50 |]
  [| "pants", 15.00 |]
  [| "hat", 5.25 |]

show table "Products" a1b3 write:"/sample/products.xlsx" with
  Products.Product
  Products.Price
```

In the above script, the path for the exported file ends with `.xlsx`, and as a result, a spreadsheet is created instead of a flat text file.

The Lokad platform supports exporting data to a short series of file formats:

* `.csv` and `.tsv`, flat text files respectively using comma (`,`) and tabulation (`\t`) as a cell delimiter. This format is recommended when exporting data from Lokad to third party systems. There is no limit to the number of columns or lines.
* `.xlsx`, the default Excel 2007 and later workbook format. It is also possible to export multiple spreadsheets into a single workbook (more details on this in a later section). This format is only recommended when end-users expect a spreadsheet to be made available to them. This format is slower to write and read than flat text files. It is also limited to roughly one million lines.
* `.ion`, the internal binary high-performance Lokad format. This format is recommended when forwarding data from one Envision script to another. It is both more compact and faster than flat text files. There is no limit in the number of columns or lines.
* `.csv.gz` and `.tsv.gz`, flat text files (as above) but compressed with the _gzip_. This format produces smaller files - due to compression - but files are substantially slower to write - and later read as well. This format is recommended when exporting data from Lokad to third party systems when either data is highly redundant, or when network bandwidth is a constraint. There is no limit to the number of columns or lines.

Attempting to export a file with an unknown filename extension results in a runtime error.

While all our examples so far are leveraging text literals for export paths, the value passed to the `export` attribute can be an arbitrary scalar text expression, as illustrated by:

```envision
table Products = with
  [| as Product, as Price |]
  [| "shirt", 10.50 |]
  [| "pants", 15.00 |]
  [| "hat", 5.25 |]

Products.Path = "/sample/products-\{Products.Product}.xlsx"

show table "Products" a1b3 write: min(Products.Path) with
  Products.Product
  Products.Price
```

The above script produces a file at the path `/sample/products-hat.xlsx`. While the above script does not really reflect a meaningful use case, this feature comes in handy for many situations. For example, when there are multiple files to be exported, it is possible to define a path for the destination folder, and then re-use this path in every export statement, as illustrated by:

```envision
exportPath = "/sample"

table Products = with
  [| as Product, as Price |]
  [| "shirt", 10.50 |]
  [| "pants", 15.00 |]
  [| "hat", 5.25 |]

show table "Products" a1b3 write:"\{exportPath}/products.xlsx" with
  Products.Product
  Products.Price
```

So far, when the `write` option was used, the table displayed in the dashboard and the table exported to the filesystem were essentially identical in their structure: same lines and same columns. However, it is possible to exclude a column from the file export.

```envision
table Products = with
  [| as Product, as Price |]
  [| "shirt", 10.50 |]
  [| "pants", 15.00 |]
  [| "hat", 5.25 |]

show table "Products" a1b3 write:"/sample/products.xlsx" with
  Products.Product
  Products.Price write:false
```

In the above script, the `write` option is used twice: first, at the tile level to indicate that the table should be exported, second, at the column level to indicate that this column should _not_ be exported. In the dashboard, the table `Products` has two visible columns, `Product` and `Price`. In the filesystem, the file `products.xlsx` has only a single column `Product`.

The default value of the _column-level_ `write` option is `true`. This option indicates whether the column should be part of the file export.

_Advanced remark:_ Under the hood, the filesystem of Lokad behaves like a Git repository. All changes are both atomic and versionned.

## Flat text file write options

When exporting data to a flat text file, compressed or not, Envision provides some capabilities to control the format of the resulting file.

The following script produces a CSV file without headers, with a US-style date format and using the dot as the decimal separator:

```envision
table Values = with
  [| as MyDate,         as MyNumber |]
  [| date(2020, 8, 4),  12          |]
  [| date(2020, 8, 4),  123.4       |]
  [| date(2020, 8, 4),  1234.56     |]

show table "My Values" a1c5 write:"/sample/values.csv" \
    omitHeaders:true date:"M/d/yy" number:"0.0" with
  Values.MyDate
  Values.MyNumber
```

This behavior is achieved through the options `omitHeaders`, `date` and `number` which can be listed in any order after the position of the tile. The resulting flat text file is the following:

```csv
8/4/20,12
8/4/20,123.4
8/4/20,1234.56
```

More generally, we have the following options:

<style>
.fmt table th:first-of-type {
    width: 10%;
}
.fmt table th:nth-of-type(2) {
    width: 10%;
}
.fmt table th:nth-of-type(3) {
    width: 10%;
}
.fmt table th:nth-of-type(4) {
    width: 70%;
}
</style>

<div class="fmt">

| Option         | Type    | Default      | Comment |
|----------------|---------|--------------|---------|
| `separator`    | text    | N/A          | Defines the separator to be used between cells. Default is comma for CSV files and tab for TSV files. |
| `omitHeaders`  | boolean | false        | Indicates whether the column headers should be inserted as the first line of the file. |
| `date`         | text    | "yyyy-MM-dd" | Format specifier to format dates. This option follows the same syntax as the one used for the `date` option on the `read` side. |
| `number`       | text    | "0.0"        | Format specifier to format numbers. This option follows the same syntax as the one used for the `number` option on the `number` side. |
</div>

These options are only available to flat text files because they do not make sense for strongly-typed formats like Ionic. Also, these options are only available for the `table` tile when the option `export` is present because they only influence the exported file.

## Pack multiple spreadsheets in a workbook

Excel workbooks have the capability to contain multiple sheets. Envision takes advantage of this capability by allowing multiple tables to be exported in the same workbook, i.e. in the same Excel file.

The following script creates a single file named `book.xlsx` with two sheets respectively named `My Products` and `My Variants`:

```envision
table Products = with
  [| as Product, as Price |]
  [| "shirt", 10.50 |]
  [| "pants", 15.00 |]
  [| "hat", 5.25 |]

table Variants = with
  [| as Product, as Color |]
  [| "shirt", "white" |]
  [| "shirt", "pink" |]
  [| "pants", "blue" |]
  [| "pants", "black" |]
  [| "hat", "red" |]

show table "Sheet 1" a1c3 write:"/sample/book.xlsx{My Products}" with
  Products.Product
  Products.Price

show table "Sheet 2" d1f3 write:"/sample/book.xlsx{My Variants}" with
  Variants.Product
  Variants.Color
```

The destination sheet is specified via the `write` option by suffixing the sheet name between the curly brackets `{` and `}`.

In the workbook, the sheets are ordered according to their order of appearance within the Envision script. In the example above, `My Products` appears first because its matching tile statement appears prior to the other tile statement.
