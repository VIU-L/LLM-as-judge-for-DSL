+++
title = "Files"
+++

## Files, built-in table

The `Files` table contains the list of all the files that have been captured by the `read` statements in the Envision script. It has a primary dimension named `file : ordinal`.

This table is intended to support the design data integrity checks. For example, to test files against conditions related to their expected size; or to pinpoint the origin file of an inconsistent line.

```envision
show table "My Files" with
  Files.Path
  Files.Age
  Files.ModifiedDate
  Files.ModifiedHour
  Files.ModifiedMinute
  Files.Alias
  Files.Bytes
  Files.Success
  Files.RawLines
  Files.BadLines
  Files.BadDates
  Files.BadNumbers
  Files.MissingValues
```

The fields are defined as follow:

* `Files.Path : text`: the original path of the file
* `Files.Age: number`: The fractional age in hours since the modified date of the file and the start of the run.
* `Files.ModifiedDate : date`: the "last modified" date of the file.
* `Files.ModifiedHour : number`: the "last modified" hour of the file, in the UTC+00 time zone.
* `Files.ModifiedMinute : number`: the "last modified" minute of the file.
* `Files.Alias : text`: the name of the table associated with file.
* `Files.Bytes : number`: the original file size, in bytes.
* `Files.Success : boolean`: whether the file was successfully loaded.
* `Files.RawLines : number`: the number of lines in the file, including those that were dropped (e.g. missing `id` or `date` values).
* `Files.BadLines : number`: the number of lines dropped - so `RawLines - BadLines` is the size of the actual file processed.
* `Files.BadDates : number`: the number of _bad date_ errors.
* `Files.BadNumbers : number`: the number of _bad number_ errors.
* `Files.MissingValues : number`: the number of _missing value_ errors.

The table `Files` is upstream of all the tables obtained through `read` statements. The following script illustrates this capability:

```envision
read "/sample/Orders*.tsv" as Orders with
  Quantity : number

Orders.Path = Files.Path // broadcast

where Orders.Quantity < 0
  show table "Files with negative order quantities" with
      Orders.Path
      group by Orders.Path
```

### Read discards

The built-in table `Files` can be used to list files irrespectively of their content, typically to check the presence or the absence of files. The _read discard_ is a syntax intended make more of the `Files` table.

```envision
read "/sample/product*" as _

show table "Files" a1b3 with
  Files.Path
  Files.Alias
```

In the above script, `_` is used as a _discard_. The resulting table cannot be further used in the script. However, the name appears in the `Files.Alias` column.

```envision
read "/sample/product*" as _products
read "/sample/order*" as _orders

show table "Files" a1b3 with
  Files.Path
  Files.Alias
```

In the above script, the discards are named respectively `_products` and `_orders`. Those tables cannot be further used in the script, but their names are preserved through `Files.Alias` to identify the original capture pattern.

A read block that does not capture any file fails in Envision - except if the files are discarded. If a discard is used, then it is valid not to capture any file. This behavior can be used to verify that a folder is empty for example.
