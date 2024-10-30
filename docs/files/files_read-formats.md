+++
title = "Read formats"
description = ""
weight = 4
+++

<!-- TODO: [vermorel] 2021-11-05 This page should be upgraded toward 'write' statements. -->
So far, Envision has been used to read and write CSV files, however the Lokad platform supports reasonably diverse file formats beyond CSV. The choice of the formats has been driven by situations that Lokad has encountered while dealing with real supply chains. Most of the formatting options, both for read and write, resolve around flat text files that are ubiquitous in supply chains _for good reasons_ (simplicity, portability, scalability, etc). However, as the notion of flat text files is relatively vague, Envision provides the capabilities to cope with all the variants that are encountered in practice.

Spreadsheets represent the second most important format, more specifically the Microsoft Excel 2007 file format, i.e. the `.xlsx` format. This format is tricky - to say the least - because there is a fine line between too little capabilities and too many capabilities. Indeed, spreadsheets can spread programs (macros) leading to various security problems. Also, some features are simply not suitable for a production data pipeline, such as embedding a spreadsheet file _within_ another spreadsheet file.

Finally, the last notable format is the _platform-specific binary format_ of Lokad known as Ionic. This format has a strong affinity to Envision itself: it is strongly-typed and its datatypes mirror those of Envision. This format has also a strong affinity to Lokad’s data processing infrastructure, which yields superior performance compared to the other formats.

As a rule of thumb, flat text files are the best for system-to-system interop, spreadsheets are the best when end-users create and modify the files, and Ionic is the best for all the inter-script communications within the Lokad platform itself.

_Advanced remarks_: Our list of supported file formats is a relatively mature feature area in the Lokad platform. Format-wise, it has been a few years since we added anything major. For example, while XML and JSON are well-known formats, they tend to be absent in most supply chain setups, and those formats tend to be (nearly) unsupported by the surrounding toolchain - which goes beyond Lokad. This does not imply that Lokad won’t ever add any extra formats, merely that we follow the dominant trends in this specific software ecosystem.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Table level read options

The read options at the _table level_ typically control the overall parsing behavior of the input files. As a rule of thumb, whenever one ends up resorting to those options, the input files can be reasonably considered as non-mainstream, one way or another. Envision has default behaviors that match sound and widespread practices concerning flat files. Thus, prior to using those options, it’s usually worth investigating whether the format can be adjusted upstream.

The following script revisits the parsing of the CSV file previously generated, but spells out the default parsing settings.

```envision
read "/sample/products.csv" \
    fileformat: "csv" quotes: false skip: 0 separator: "," as Products with
  Product : text
  Price : number

show table "Products" with
  Products.Product
  Products.Price
```

Within the `read` statement, the table-level options follow the file pattern adopting a `key: value` syntax. The first line of the above script ends with `\` which is a line continuation, only used for aesthetic purposes to break a line that would otherwise be quite long.

All the values have to be specified as literals. Unlike the file pattern itself, compile-time constants cannot be used. The following options are available:

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
    width: 10%;
}
.fmt table th:nth-of-type(5) {
    width: 60%;
}
</style>

<div class="fmt">

| Option       | Type    | Default | Type of file  | Comment |
|--------------|---------|---------|---------------|---------|
| `fileformat` | text    | N/A     | any           | Applies the specified extension to all input files. Any recognizable extension, e.g. `csv` or `xslx` can be specified. This option overrides the default auto-detection of the file format. |
| `skip`       | number  | 0       | text or Excel | Indicates how many lines should be skipped at the beginning of each file while files are being read. This option is intended for situations where the first lines are not yet the tabular data, but typically control or are the heading lines. |
| `encoding`   | text    | N/A     | text          | Specifies the text encoding to be used while parsing files. See below for the list of accepted encoding values. The option overrides the default auto-detection of the file encoding. |
| `headers`    | text    | N/A     | text          | Specifies the heading line to be used instead of the first line found in every file. These headers are intended to list the column found in the file. If headers are specified to override existing headers - as opposed to cope with missing ones - then `skip: 1` should be used. |
| `quotes`     | boolean | false   | text          |  If `false` then Envision escapes extreme quotes, as is usually done with CSV (comma-separated values) files. If `true` then the extreme quotes found in a cell token are considered to be part of the token and not escaped. |
| `separator`  | text    | N/A     | text          | Indicates the separator between cell values to be used when parsing files. This option overrides the default auto-detection that determines the most likely cell separator. |
| `date`      | text    | N/A     | text           | Format specifier to parse dates. This option overrides the default auto-detection that determines the most likely date format. |
| `number`  | text    | N/A     | text             | Format specifier to parse number. This option overrides the default auto-detection that determines the most likely number format. |

</div>

The list values accepted for the `encoding` option are:

* `ibm861` (Icelandic code page)
* `ibm865` (Nordic code page)
* `ISO-8859-1`
* `latin1` (alias of `ISO-8859-1`)
* `UTF-8`
* `UTF-16`
* `Windows-1250` (ANSI Central Europe)
* `Windows-1252` (ANSI West Europe)

The default behavior of several options - e.g. `fileformat` - cannot be obtained explicitly, only implicitly, by omitting the option altogether. These situations are associated with the auto-detection heuristics used by Envision that are - to a limited extent - loosely specified. On the contrary, once an option is specified, it follows a rigid behavior that is guaranteed to be enforced. Nevertheless, we recommend not specifying these options unless necessary. In our experience, these auto-detection heuristics are reliable and compatible with a production-grade data pipeline.

The file format analysis is based on the file name extension, and goes in several stages. If the file name ends with `.xlsx` or `.ion`, then the file is recognized as an Excel spreadsheet or an Ionic file respectively. If the file name ends with `.csv`, `.tsv`, `.txt`, `.csv.gz`, `.tsv.gz` or `.zip` then, the file is recognized as _flat text file_. Unless a `fileformat` is specified, any other file name ending is considered as unknown, and leads to a parsing failure.

If the file name ends with `.csv.gz`, `.tsv.gz` or `.zip`, then, the file is _decompressed_ respectively through the GZIP or ZIP formats. While ZIP is an _archive_ format, Envision expects that the archive only contains a single file, and will fail otherwise. These files are decompressed, and the parsing resume.

When parsing a flat text file, unless specified otherwise, Envision automatically detects its format (e.g. separator, numbers and dates). In particular, whether the file is named `.csv` or `.tsv` has no impact on those format detection heuristics, not even for the choice of the value separator.

As a tangential remark, _header-free flat files should be avoided wherever possible_. While the `headers` option is available to cope with such files, relying on the option invariably makes the data pipeline fragile. Without headers, it becomes difficult to investigate any versioning problem related to file formats. For example, the inversion of two columns (assuming that the columns have the same data type) can silently permeate the data pipeline and corrupt most later calculations.

The fine print of the `date` and `number` attributes is detailed in the next section.

_Advanced remark:_ The GZIP and ZIP format should not be confused. ZIP is an _archive_ format, and was historically associated with the WinZip utility on Microsoft Windows. GZIP is a pure compression format, and was historically part of the default GNU/Linux utilities. As a rule of thumb, the GZIP format is typically more appropriate for most data pipeline use cases. ZIP may have a role when end-users have to routinely manually upload large flat text files to Lokad while not having access to high-speed internet connections. In those cases, the ZIP format can alleviate some of the upload overhead. ZIP is somewhat of a second-class citizen from the Lokad perspective because we don’t embrace - on purpose - the _archive_ nature of the format.

**Roadmap**: the table-level read options are _required_ to be literals rather than compile-time constants, however, we intend to lift this constraint in the future.

## Date and number options

Envision supports two mini-syntaxes respectively dedicated to the formatting (and parsing) of dates and numbers. Two syntaxes are invoked via the attributes `date` and `number` that we introduced in the previous section.

Let’s illustrate this capability with two following scripts. The first script generates a flat file named `products.csv` with two formatting conventions for dates and numbers respectively:

```envision
table Products = with
  [| as Product, as Price, as LaunchDate |]
  [| "shirt", 10.50, date(2020, 06, 25) |]
  [| "pants", 15.00, date(2020, 07, 12) |]
  [| "hat",   5.25,  date(2020, 08, 04) |]

show table "Products" write:"/sample/products.csv" \
    date:"yy/MM/dd" number:"0,0" with
  Products.Product
  Products.Price
  Products.LaunchDate
```

Then, the second script reads the file named `products.csv` with the same two formatting conventions, again for dates and numbers respectively:

```envision
read "/sample/products.csv" \
    date:"yy/MM/dd" number:"0,0" as Products with
  Product : text
  Price : number
  LaunchDate : date

show table "Products" with
  Products.Product
  Products.Price
  Products.LaunchDate
```

In the scripts above, the `date` format indicates that the date will be composed of the year (two digits), followed by the month (two digits), followed by the day (two digits), using the slash `/` as the separator. Similarly, the `number` format indicates that no thousand separator is used, but that the comma `,` is used as the decimal separator.

More generally, the syntax for `date` follows:

* `d`: day of the month from 1 through 31.
* `dd`: same as `d` but 0 prefixed.
* `ddd`: abbreviated day of the week (ex: Mon, Tue...).
* `dddd`: full day of the week (ex: Monday, Tuesday...).
* `M`: month number from 1 through 12.
* `MM`: same as `M` but 0 prefixed.
* `MMM`: abbreviated name of the month (ex: Jan, Feb, ...).
* `MMMM`: full name of the month (ex: June).
* `yy`: year number from 00 to 99, ignore the hundreds and thousands.
* `yyyy`: year with four digits (ex: 2020).

The syntax for `number` is as follows (`Y` represents the number decimal separator and `X` the thousand separator):
* "Y", `X` is set to `,` unless it is `Y`'s value, then it is set to `.`.
* "XY"
* "0Y0", `X` is set to `,` unless it is `Y`'s value, then it is set to `.`.
* "1X000Y0"

Envision provides a symmetric behavior on the read and write sides. If a specified format is used to write data, assuming no data gets lost, then the same data can be read with the same options.

These formatting and parsing behaviors should not be confused with presentation behaviors offered by StyleCode, which will be covered in greater detail in a later section. These options only impact how data is read from files and how it is written to files. The appearance of the dashboard is not impacted by those options.

## Renaming read columns

The name of a column, as found in the flat file, may not be a valid variable name in Envision. Thus, Envision provides a mechanism to rename columns as found in input files. So far, we have only seen the basic column read syntax, as illustrated by:

```envision
read "/sample/products.csv" as Products with
  Product : text
  Price : number
```

In the above script, there are two _column reads_, `Product : text` and `Price : number`. The column name comes first, followed by a semicolon and the data type.

The flat files and spreadsheets are restricted to the following data types, both for read and write: `text`, `number`, `date`, `boolean`. Ionic files support all data types except `markdown`. Specifying the data type is mandatory in Envision.

Let’s refresh the file `products.csv` with the following script:

```envision
table Products = with
  [| as Product, as Price |]
  [| "shirt", 10.50 |]
  [| "pants", 15.00 |]
  [| "hat", 5.25 |]

show table "Products" write:"/sample/products.csv" with
  Products.Product as "My Product"
  Products.Price
```

The above script is almost identical to the one we had introduced in a previous section, except for the line `Products.Product as "My Product"` which specifies `"My Product"` as an alternative column name in the file to be exported. This name is precisely chosen because it is not compatible with an Envision variable name due to its inner whitespace. There are many more write options, we will revisit those in a later section.

The syntax we have introduced so far would not be compatible with such an invalid column name, however, this situation can be addressed with:

```envision
read "/sample/products.csv" as Products with
  Product : text = read("My Product")
  Price : number
```

The above script leverages the `read` keyword in order to introduce `"My Product"` as the text literal that will be used to match the column name as found in the file. If this script is executed right after the previous one, the sequence works.

Unlike valid variable names, the text literal specified through `read` can be any text value, including whitespaces or accentuated characters for example. 

Also, although doing so is not recommended, it is possible to read the column based on its position in the file, using a numeric argument: 

```envision
read "/sample/products.csv" as Products with
  Product : text = read(1)
  Price : number
```

Here, 1 represents the leftmost column, 2 is the second leftmost, and so on. Using positions instead of names is brittle, and can easily break if the file format is changed. 

## Reading heterogeneous files

When reading a single table from many files, all its underlying files may not have the same columns. For example, the `Orders` table might be the consolidation of the data obtained from a now-defunct legacy ERP and from the current one. The respective file formats may be close enough to warrant a unified read, and yet, the subtle differences between the formats need to be accounted for.

Let’s consider a situation where the list of products is spread over two files `products.csv` and `goods.csv` that exhibit divergent column names as illustrated by:

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

show table "Products" write:"/sample/products.csv" with
  Products.Product
  Products.Price

show table "Products" write:"/sample/goods.csv" with
  Goods.Good
  Goods.Price
```

The file `products.csv` has two columns `Product` and `Price`, while the file `goods.csv` has the columns `Good` and `Price`. Let’s see how these two files can be consolidated into a single `Products` table. This process is illustrated with:

```envision
read "/sample/products.csv" as Products with
  Product : text
  Price : number

read "/sample/goods.csv" as Products with
  Product : text = read("Good")

show table "" a1c3 with
  Products.Product
  Products.Price
```

In the above script, the first `read` statement is identical to the one we have seen in a previous section. However, the second `read` statement, the one that focuses on `goods.csv` is quite different. This second block is also associated with the `Products` table, but only a single column is specified, and it’s precisely the column that needs to be renamed from `Good` to `Product`.

A single table can be produced from multiple `read` statements. The first `read` statement must specify all the columns, their types and all the relationships (i.e. primary and foreign dimensions) of the table. Later the `read` statement should only list the _divergences_.

<!-- [vermorel] 2020-08 TODO: not working yet, but should. https://lokad.atlassian.net/browse/LK-6707 -->

Also, it is possible to supplement one or several columns that happen to be missing from files. Let’s assume that the column `Price` is missing from the file `products.csv` while the column `Product`  is missing from the file `goods.csv`. The following script addresses this situation:

```envision
read "/sample/products.csv" as Products with
  Product : text
  Price : number = 11.5

read "/sample/goods.csv" as Products with
  Product : text = "hat"

show table "" a1c3 with
  Products.Product
  Products.Price
```

An assignment is used to replace the `Price` column with a constant set at `11.5` and then it is used to replace the `Product` column with the constant text literal `hat` .

More generally, any compile-time constant can appear on the right side of an assignment.

## Column-merging read

Within a flat text file, a set of columns may represent the same value associated with different contexts. For example, a file could contain a product identifier column, and then twelve "product sales for month N" columns. Let's consider the following script that produces three "year" columns for a price value: 

```envision
table Products = with 
  [| as Product, as PriceYearN, as PriceYearN1, as PriceYearN2 |]
  [| "shirt",    10.50,         10.00,          10.00          |]
  [| "pants",    15.00,         14.00,          14.50          |]
  [| "hat",       5.25,          5.50,           5.75          |]

show table "Products" write:"/sample/products.csv" with 
  Products.Product
  Products.PriceYearN as "Price (Y)"
  Products.PriceYearN1 as "Price (Y-1)"
  Products.PriceYearN2 as "Price (Y-2)"
```

In order to read all three columns as a single column, the `read()` binding can be used with several columns:

```envision
read "/sample/products.csv" as Products with 
  Product : text
  Price : number = read("Price (Y)", "Price (Y-1)", "Price (Y-2)")

Products.Year = year(today()) - count(Products.*) by Products.Product scan auto

show table "Products" a1c3 with
  Products.Product
  Products.Year
  Products.Price
```

For each line in the original file, this script will read three lines. The column `Product` is the same across all three lines, and the column `Price` will take the value of the in-file columns "Price (Y)", "Price (Y-1)" and "Price (Y-2)", in that order. 

The ordering of the columns ensures that a `count(*) scan auto` can be used to number these lines from 0 to 2.

## Multi-value column read

Within a flat text file, a single column may contain multiple values, typically separated by a separator that happens to be distinct from the primary separator of the file. Let’s consider the following script that produces a CSV  file where the `Colors` column implicitly contains a list of values.

```envision
table Products = with
  [| as Product, as Colors, as Price |]
  [| "shirt", "white;pink",      10.50 |]
  [| "pants", "black;blue;grey", 15.00 |]
  [| "hat",   "brown",            5.25 |]

show table "Products" write:"/sample/products.csv" with
  Products.Product
  Products.Colors
  Products.Price
```

This file can then be read with the following script that leverages the `split` option.

```envision
read "/sample/products.csv" as Products with
  Product : text
  Color : text = read("Colors") split:";"
  Price : number

show table "Products" a1c3 with
  Products.Product
  Products.Color
  Products.Price
```

The `split` option follows the `read()` construct in the definition of the read column. It is followed by a text literal that defines the expected separator. Also, for the sake of clarity, the column `Colors` is renamed `Color` (singular) because, due to the split, there is only one color left per line in every `Product.Color` value.

Only a single `split` option can be specified per table. This limitation is enforced by Envision in order to steer clear from pathological behaviors, where a single line in the original text file could end-up being multiplied into an arbitrary large number of generated lines. Ex: if two values on the same line were to be split into 10 sub-values each, then this would result in 10x10=100 pairs.

_Advanced remarks_: Envision text values are limited to 256 characters. However, the `split` read option has been designed in such a way that it is possible to reach a flat file that happens to exhibit cell values larger than 256 characters, as long as those cells are split and that the resulting sub-values are individually shorter than 256 characters.

## Sanitizing input files

Existing flat file exports may come with all sorts of quirks. For example, missing values may get written in the files as `null`, or some numbers may come with an unusual representation. The role of a sanitization process is to extract a sensible subset of the input data that isn’t entirely sane. When facing somewhat pathological situations, the recommended path in Envision consists of reading the columns as `text`, and then applying the parsing logic within the script itself.

Let’s consider the file `products.csv` generated by the following script:

```envision
table Products = with
  [| as Product, as Size |]
  [| "shirt",   "4,5" |]
  [| "pants",  "null" |]
  [| "hat",     "3,2" |]

show table "Products" write:"/sample/products.csv" with
  Products.Product
  Products.Size
```

The `Size` column contains two oddities. First, there are `null` values that cannot be parsed into numbers in a meaningful way. Second, the decimal separator is the comma (`,`) instead of being the default dot (`.`).

The file can then be read with `Size` as a raw text column as illustrated by the following script:

```envision
read "/sample/products.csv" as Products with
  Product : text
  SizeRaw : text = read("Size")

Products.IsSizeDefined, Products.Size =
  tryParseNumber(Products.SizeRaw, "", ",")

show table "Products" a1c3 with
  Products.Product
  Products.SizeRaw
  Products.IsSizeDefined
  Products.Size
```

The function `tryParseNumber` takes three arguments: first, the text values to be tentatively parsed as numbers, second, the thousand’s separator, third, the decimal separator. It returns two arguments as a tuple. The first value of the tuple is a `boolean` that indicates whether the text value has been successfully parsed as a number. The second value of the table is a `number`, which gives the result of the parsing, but only when the parsing has been successful, and otherwise is the default number value (i.e. zero).

Envision also provides the function `parseNumber`, which always expects the parsing operation to succeed (and fail otherwise) as well as the functions `parseDate` and `tryParseDate`, which are the counterparts to what we have seen in this section but for dates instead.
