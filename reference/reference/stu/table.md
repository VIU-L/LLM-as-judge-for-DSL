+++
title = "table"
+++

## table, keyword

The `table` keyword indicates that the statement reflects the creation of a table.

```envision
table T = extend.range(10)
show table "My Range" a1a8 with T.N
```

There are multiple ways to create a table from another table, such as the `by` statement.

```envision
table T = extend.range(10)
table U[u] = by T.N mod 4
show table "My Range" a1a8 with u
```

Or the `where` statement:

```envision
table T = extend.range(10)
table U = where T.N < 5
U.N = T.N
show table "My Range" a1a8 with U.N
```

## table, tile type

The `table` tile is the most versatile tile offered by Envision. This tile is intended to display a table, and this table can optionally be exported as a flat file.

```envision
table T = with
  [| as Product, as Price, as StartDate      |]
  [| "Hat"     , 42.25   , date(2022, 1, 1)  |]
  [| "Pant"    , 59.95   , date(2022, 1, 1)  |]
  [| "Shoe"    , 49.90   , date(2022, 2, 17) |]

show table "Products" a1c3 with
  T.Product
  T.Price
  T.StartDate
```

The tile can be sorted with the `order by` option.

```envision
table T = with
  [| as Product, as Price, as StartDate      |]
  [| "Hat"     , 42.25   , date(2022, 1, 1)  |]
  [| "Pant"    , 59.95   , date(2022, 1, 1)  |]
  [| "Shoe"    , 49.90   , date(2022, 2, 17) |]

show table "Products" a1c3 with
  T.Product
  T.Price
  T.StartDate
  order by T.Price desc
```

The tile can internally perform an aggregation with the `group by` option.

```envision
table T = with
  [| as Product, as Price, as StartDate      |]
  [| "Hat"     , 42.25   , date(2022, 1, 1)  |]
  [| "Pant"    , 59.95   , date(2022, 1, 6)  |]
  [| "Shoe"    , 49.90   , date(2022, 2, 17) |]

show table "Products" a1c3 with
  count(T.*) as "Launched"
  T.StartDate
  group by T.StartDate
```

### Tile-level options

The table tile supports options defined at the _tile-level_.

```envision
table T = with
  [| as Product, as Price, as StartDate      |]
  [| "Hat"     , 42.25   , date(2022, 1, 1)  |]
  [| "Pant"    , 59.95   , date(2022, 1, 1)  |]
  [| "Shoe"    , 49.90   , date(2022, 2, 17) |]

show table "Products" a1c3  date: "MM-dd-yyyy" write:"/sample/products.csv" with
  T.Product
  T.Price
  T.StartDate
```

The list of options available are:

* `date` (scalar text): the default date format for dates columns. This option only applies to the file being written.
* `download` (scalar text): the default file name used when the tile is downloaded by a user from the dashboard.
* `write` (scalar text): the file path where the content of the table gets stored within the Lokad account. For example "`write:"/foo/bar.csv"`. When multiple `write` options are present; multiple files will be written accordingly.
* `number` (scalar text): the default number format for numeric columns. This option only applies to the file being written.
* `quotes` (scalar Boolean): when `true`, forces quotes around the data in generated CSV or TSV files. The default value is `false`.
* `freezeFirstColumn` (scalar Boolean): when `true`, freeze the first colum in the downloadable Excel export of the tile.

### Column-level options

The table tile supports options defined at the _column-level_.

```envision
table T = with
  [| as Product, as Price, as StartDate      |]
  [| "Hat"     , 42.25   , date(2022, 1, 1)  |]
  [| "Pant"    , 59.95   , date(2022, 1, 1)  |]
  [| "Shoe"    , 49.90   , date(2022, 2, 17) |]

show table "Products" a1c3  write:"/sample/products.csv" with
  T.Product
  T.Price excelformat: "#,##0.00\ [$₽-419]"
  T.StartDate write:false
```

<!-- The options 'date' and 'number' should probably be phased-out:
https://lokad.atlassian.net/browse/LK-11394 -->
The list of options at the column level are:

* `date` (scalar text): the date format for this column. This option only applies to the file being written.
* `excelFormat`(scalar text): the formatting text value, as specified by Microsoft Excel, to be applied to the matching cells within the spreadsheet that can be downloaded from the dashboard.
* `number` (scalar text): the number format for a numeric column. This option only applies to the file being written.
* `quotes` (scalar Boolean): when `true`, forces quotes around the column data in generated CSV or TSV files. The default value is `false`.
* `write` (scalar Boolean): indicates whether the column will be written to a file. The default value is `true`. Not writing a column can be of interest if the intent is only to display the column in the dashboard.
