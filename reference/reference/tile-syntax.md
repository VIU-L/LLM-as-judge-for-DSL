+++
title= "Tile syntax"
weight= 5.5
+++

<!-- TODO: 'Tile syntax' belongs to the 'Language' section, and must be rewritten -->

The tiles represent the building blocks of Envision's dashboards. Below, we detail the generic syntax of the tiles, how tiles can be used to write data to files, how descriptive metadata can be attached to those writes, and how to create the slices for a dashboard.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Syntax overview

The generic syntax for a tile is:

```envision-proto
show table "my title" a1c2 tomato slices: SX {backgroundColor: "#fdad31"} with
  Items.Category as "My category"
  Items.Supplier as "My supplier"
  sum(Items.StockOnHand) as "Stock on hand"
  sum(Items.StockOnHand * BuyPrice) as "Stock value"
  group by [Items.Category,Items.Supplier]
  order by [Items.Category, sum(Items.StockOnHand * Items.BuyPrice)] desc
```

The elements that compose a tile are as follow:

* a _tile type_ - `table` here above - which defines the type of tile to be displayed.
* a _tile title_ - `my title` here above - which defines a label intended to display prominently.
* a _tile position_ (optional) - `a1c2` here above - which defines both the tile and its size within the dashboard over an Excel-like grid: letters refer to column, numbers to lines.
* a _tile color_ (optional) - `tomato` here above - which is expected to either a named  [web colors](https://en.wikipedia.org/wiki/Web_colors), or as a hex color name but without the `#` sign (ex: `FF6347` for tomato).
* a _slice option_ (optional) - a `slices: SX` here above - which indicates that the tile display depends on the selected slice.
* a _stylecode expression_ (optional) - `{backgroundColor: "#fdad31"}` - which is delimited by `{` and `}`, and which configures the display behavior of the tile (check out [StyleCode reference](/reference/stylecode/)).

The expressions passed as arguments after the `with` keyword are automatically aligned by Envision, in order to treat the input data as a table for the tile (not just for `table` tiles, but for all tiles). In order to set up the grouping and ordering of lines within this input table, an _optional_ statement can be added at the end of the column list:

* The `group by` statement applies the same grouping to all fields. When `group by` is used, expressions must expose aggregators (`sum()`, in the example above). If they are pre-aggregated already, they have to be introduced by the aggregator `same()`.
* The `order by` statement orders the lines in increasing order. Decreasing order is obtained by the additional optional statement `desc`.

Both `group by` and `order by` are optional and support multiple arguments. In addition, `order by` supports multiple arguments with multiple directions, e.g.:

```envision-proto
show table "my table" with
  T.X
  T.Y
  T.Z
  order by [T.X desc, T.Y]
```

`T.X desc` would be automatically translated to -T.X, thus will work in case of numbers, yet, will fail for non-number expressions, such as text. `T.X desc` can be used for both, numbers and non-number expressions.

Envision also offers a concise inline syntax without line returns which is appropriate for simple tiles:

```envision-proto
show table "my table" with T.X, T.Y, T.Z
```

## Writing data

The `show table` tile can be written to a file using the `write` option:

```envision-proto
show table "hello" a1c2 tomato write:"/foo2.tsv" with
  Items.Category
  Items.Supplier
  sum(Items.StockOnHand) as "Stock on Hand"
  sum(Items.StockOnHand * Items.BuyPrice) as "Stock Value" {unit: "$"}
  group by [Items.Category,Items.Supplier]
  order by [Items.Category, sum(Items.StockOnHand * Items.BuyPrice)] desc
```

Supported write formats are:

* `.csv` and `.tsv` flat files
* `.csv.gz` and `.tsv.gz` compressed flat files
* `.ion` Ionic file format (Lokad)
* `.xlsx` Excel files; the sheet name can be specified in braces after the name: `foo.xlsx{Sheet A}`.

Two tiles may not write to the same file path. As an exception, they may write into the same Excel file, but not into the same sheet. All the spreadsheets within one Excel file will be alphabetically ordered.

It is also possible to write the tile data to several locations at once, using multiple `write` statements:

```envision-proto
show table "hello" a1c2 tomato write:"/foo1.tsv" write:"/foo2.tsv" with
  Items.Category
  Items.Supplier
  sum(Items.StockOnHand) as "Stock on Hand"
  sum(Items.StockOnHand * Items.BuyPrice) as "Stock Value" {unit: "$"}
  group by [Items.Category,Items.Supplier]
  order by [Category, sum(Items.StockOnHand * Items.BuyPrice)] desc
```

## Attaching meta descriptions to writes

When a file is produced through Envision, it is possible to attach descriptive metadata to this file and its columns. Those metadata are optional. Those descriptions are intended to facilitate later data manipulation of the file itself by making the descriptions accessible from the Envision code editor itself. Attaching those descriptions can be done with well placed `///` triple-slash comment, as illustrated with:

```envision-proto
/// Stock value summary table
show table "hello" a1c2 tomato write:"/foo1.tsv" write:"/foo2.tsv" with
  Items.Category
  Items.Supplier
  /// Stock on hand by category and supplier
  sum(Items.StockOnHand) as "StockQty"
  /// Stock on hand value by category and supplier
  sum(Items.StockOnHand * Items.BuyPrice) as "StockValue" {unit: "$"}
  group by [Items.Category,Items.Supplier]
  order by [Items.Category, sum(Items.StockOnHand * Items.BuyPrice)] desc
```

In the Envision code editor, when hovering a variable obtained through a `read` statement, an attempt is made to locate the originating `write` which produced the variable. If such originating `write` statement is found, the descriptive metadata is contextually displayed.

 The displayed information is:

* the variable data type
* the table name and its keys (ex. `Orders expect [Id, Date]`)
* the path of the script where the variable was written
* the documentation specified about the table
* the documentation specified about the specific variable.

The first two details are available also for any new table, vector and scalar, that are created in that very script (ex. `day.qty`).

## Dashboard slicing

Each dashboard is allowed to have a slice set. Slices are numbered internally from `0` to `N-1`. The identifier of a slice is represented by a special type called `slice`. To create the slices for a dashboard, create the `Slices` table anywhere in the script (but no more than once):

```envision-proto
table Slices[slice] = slice by [Items.Category, Items.Sku] title: Items.Name
```

In this example, there will be one slice for each distinct value of the `[Category, Sku]` pair. The slice identifier assigned to each value is then inflated back into the original table (here, Items). Selecting a slice (on the dashboard user interface) consists in selecting its internal identifier by means of a form field, using auto-completion to narrow down possible choices until one can be picked. Auto-completion is based on searching through the display text of the slice, which is composed of:

* the `Name` value, which should be the same for all lines in a slice
* on a second line, the optional label passed as argument (and which must, again, be the same for all lines in a given slice).

```envision-proto
table Slices[slice] = slice by [Items.Category, Items.Sku] \
  title: Items.Name subtitle: Items.Label
```

Some tiles can be sliced by introducing a slice vector (of the same table as the tile's actual data) as the slices option, in which each slice will contain only the lines associated with it:

```envision-proto
show table "Purchase Orders" slices: Slice with
  PO.OrderId
  PO.Date
  PO.Quantity
  order by PO.Date
```

### Slicing linechart tile

Slicing the `linechart` tile requires a `group by` argument to specify the date vector against which to plot. This can be done with:

```envision-proto
table Slices[slice] = slice by id title: id subtitle: Items.Name
WeekItems.Ssice = Items.slice
WeekItems.monday = same(monday(date))

show linechart "Weekly Quantity Sold" slices: WeekItems.Slice with
  sum(WeekItems.QtySold) as "Qty Sold"
  group by WeekItems.monday
```

Notice how `Items.slice` is broadcast on `WeekItems.slice`.
