+++
title = "read"
+++

**Table of contents**
{{< toc >}}{{< /toc >}}

## read, table creation

The keyword `read` offers versatile mechanisms to read data from files.

```envision
table Products = with
  [| as Product, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]

write Products as "/sample/products.csv" with
  Product = Products.Product
  Color = Products.Color
  Price = Products.Price
```

Then,

```envision
read "/sample/products.csv" as Products with
  Product : text
  Color : text
  Price : number

show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price
```

A single script is limited to 5000 input files.

All the `read` blocks must appear at the top of the Envision script, above any statement that cannot be processed at compile-time.

```envision
// only compile-time constants can be placed above 'read'
const path = "/mytable.csv" 

read (path) as T with // parenthesis are needed here
  ColumnA : text
  ColumnB : number
```

### Constant column

A constant column can be introduced through an assignment at the column level within the `read` block:

```envision
read "/sample/products.csv" as Products with
  Product : text
  Color : text
  Price : number
  VAT : number = 0.2 // constant column

show table "My Products" a1c4 with
  Products.Product
  Products.Color
  Products.Price
  Products.VAT
```

### Renamed column

A column can be renamed through an assignment and the use of the `read` function at the column level within the `read` block:

```envision
read "/sample/products.csv" as Products with
  Product : text
  Colour : text = read("Color")
  Price : number

show table "My Products (UK)" a1c4 with
  Products.Product
  Products.Colour
  Products.Price
```

The function `read` is intended to cope with raw column names that are not valid Envision variable names.

### `split` column-level option
<!-- Odd prefix position of the 'split' option
https://lokad.atlassian.net/browse/LK-10882 -->
The option `split` splits the content of a text cell according to the specified delimiter, resulting in multiple lines being for each value obtained by the split.

| A | B   |
|---|-----|
| 1 | X,Y |
| 2 | Z   |

With a `split:","` on `B` gives:

| A | B |
|---|---|
| 1 | X |
| 1 | Y |
| 2 | Z |

The script below creates a TSV file with 2 lines:

```envision
table T = with
  [| as A, as B  |]
  [| 1,    "X,Y" |]
  [| 2,    "Z"   |]

write T as "/sample/split.tsv" with
  A = T.A
  B = T.B
```

And, the script below re-reads the TSV file generating a table with 3 lines:

```envision
read "/sample/split.tsv" as T with
  A : number
  split:"," as B : text

show table "T" a1b3 with T.A, T.B
```

The option `split` can only appear once within a `read` block.

### Transpose column-level option

When multiple values are passed to the `read` function within a `read` block, it tranposes the corresponding columns - as found in the file - in the same number of lines. The columns that are not transposed have their values repeated. For example, by transposing _(B1, B2, B3)_ in:

| A | B1 | B2 | B3 |
|---|----|----|----|
| X | X1 | X2 | X3 |
| Y | Y1 | Y2 | Y3 |

We obtain:

| A | B  |
|---|----|
| X | X1 |
| X | X2 |
| X | X3 |
| Y | Y1 |
| Y | Y2 |
| Y | Y3 |

The following script creates a TSV file with 2 lines:

```envision
table T = with
  [| as A, as B1, as B2, as B3 |]
  [| "x",  "x1",  "x2",  "x3"  |]
  [| "y",  "y1",  "y2",  "y3"  |]

write T as "/sample/transpose.tsv" with
  A = T.A
  B1 = T.B1
  B2 = T.B2
  B3 = T.B3
```

And, the script below re-reads the TSV file generating a table with 6 lines:

```envision
read "/sample/transpose.tsv" as T with
  A : text
  B : text = read("B1", "B2", "B3")

show table "T" a1b6 with T.A, T.B
```

### Discarded table

Prefixing the table name with an underscore (`_`) means that the table is discarded. However, the captured files are accessible from the `Files` built-in table.

```envision
read "/sample/*.csv" as _Samples

show table "Files" a1c2 with 
  Files.Alias // '_Samples'
  Files.Path
```

The table marked as _discarded_ cannot be used in the script, and thus, this table does not trigger a _not used_ error at compile time when it is, effectively, not used in the script.

Using a stand-alone discard symbol (`_`) is also possible:

```envision
read "/sample/*.csv" as _

show table "Files" a1c2 with 
  Files.Alias // '_'
  Files.Path
```

This feature is typically intended for scripts that are analyzing the presence or absence of files, ignoring of their content.

### Datatype read/write support

The following table lists the database that can be read or written, depending on the intended file format.

| Type     | TSV read/write | Ionic read/write |
|----------|----------------|------------------|
| boolean  | yes            | yes              |
| date     | yes            | yes              |
| markdown | no             | no               |
| month    | yes            | yes              |
| number   | yes            | yes              |
| ranvar   | no             | yes              |
| text     | yes            | yes              |
| week     | yes            | yes              |
| text     | yes            | yes              |
| zedfunc  | no             | yes              |
