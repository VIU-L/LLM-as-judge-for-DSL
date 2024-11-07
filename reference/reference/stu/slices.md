+++
title = "Slices"
+++

## Slices, built-in table

This built-in table is created by _slicing_ the dashboard. When a dashboard is sliced:

* Only a single slice is visible at a time.
* A selector appears drop-down in the upper-right corner of the dashboard.
* Individual tiles can be sliced, which causes them to display a different set of rows on each slice. This behavior is controlled via the `slices:` tile option.
* A StyleCode `#(..)` accepts vectors in the `Slices` table (and not only in the `Scalar` table), and will use a different value for each slice. This extends to other StyleCode-equivalent values, such as tile titles.

Example:

```envision
table T[t] = with 
  [| as Product, as Color |]
  [| "Pants",    "Blue"   |]
  [| "Cap",      "Red"    |]
  [| "T-shirt",  "White"  |]

table Slices[slice] = slice by t title: T.Product

{ tileColor: #(same(T.Color) into Slices) }
show table "Contents of slice" a1b3 slices: slice with
  T.Product
  T.Color 
```

The name of the slices table is always `Slices` and its primary dimension is always named `slice`. This table can be created at most once in a script.

The syntax for creation is:

```envision-proto
table Slices[slice] = slice by [tuple] title: Expr subtitle: Expr
```

All vectors are expected to be in the same table (which will automatically receive `slice` as a secondary dimension).

* The tuple determines the number and order of slices. In particular, the slice displayed when the dashboard is opened is the one with the minimum tuple value.
* The `title` is mandatory and provides a text label that will be displayed in the slice-picker drop-down in the top right of the dashboard. There must be exactly one distinct title value for each distinct tuple value.
* The `subtitle` is optional, and provides a second text label to be displayed under the title. There may be up to 255 distinct subtitle values for each distinct tuple value.

Both the title and all the subtitles can be searched through by the slices drop-down component, so having multiple subtitles makes it easier to search for slices.
