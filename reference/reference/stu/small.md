+++
title = "small"
+++

## small, contextual keyword in read statement

The option `small` can be specified after the table name in a `read` statement to indicate that the table does not spread over multiple pages. If the table size exceeds the maximum page size for any vector of the table, then the script fails. If the table size exceeds the threshold, then the script fails.

```envision
read "/sample/products.csv" as Products small 10 with
  Product : text

show table "My Products" a1b3 with Products.Product
```

The option `small` offers the possibility to specify two thresholds. The lower inclusive threshold indicates the maximum number of lines that does not generate a warning. The higher inclusive threshold indicates the maximum number of lines that does not generate an error.

```envision
read "/sample/products.csv" as Products small 2 .. 10 with
  Product : text

show table "My Products" a1b3 with Products.Product
```

The warning threshold is intended to help avoid "slowly creeping" situations and detect that a table has grown too much before it becomes a blocking problem.

## small, contextual keyword in table statement

The option `small` can be specified after the table name in a `table` assignement to indicate that the table does not spread over multiple pages. If the table size exceeds the maximum page size for any vector of the table, then the script fails.

```envision
table T small = with
  [| as A |]
  [| "b"  |]
  [| "c"  |]
  [| "a"  |]

show table "" with T.A
```

An inclusive threshold for the maximum number of lines in the table can be specified. If the table size exceeds the threshold, then the script fails.

```envision
table T small 10 = with
  [| as A |]
  [| "b"  |]
  [| "c"  |]
  [| "a"  |]

show table "" with T.A
```

The `small` option offers the possibility to specify two thresholds. The lower inclusive threshold indicates the maximum number of lines that does not generate a warning. The higher inclusive threshold indicates the maximum number of lines that does not generate an error.

```envision
table T small 2 .. 10 = with
  [| as A |]
  [| "b"  |]
  [| "c"  |]
  [| "a"  |]

show table "" with T.A
```

The warning threshold is intended to help avoid "slowly creeping" situations and detect that a table has grown too much before it becomes a blocking problem.

### See also

* [max](../../mno/max/)
