+++
title = "as"
+++

The keyword `as` generally serves postfix variable assignments in Envision.

## 'read "path" as tblName', table naming in 'read' block

The keyword `as` is used to name a table in a `read` block:

```envision
read "/mytable.csv" as T with // table named 'T'
  ColumnA : text
  ColumnB : number
```

## '(text) as (variable)', column renaming in 'read' block

The keyword `as` is used to rename a column that appears in the flat file:

```envision
read "/mytable.csv" as T with
  "Column A" as ColumnA : text // rename 'Column A' as 'ColumnA'
  "Bar" as Foo : number // rename 'Bar' as 'Foo'
```

The intent of this feature is to support flat files even when their column names are not compatible with Envision's variable naming rules. For example, `Column A` is not a proper variable name in Envision as it contains a whitespace; but with the `as` keyword, it gets renamed as `ColumnA` which is a proper Envision name.

## 'as (variable)', column definition in table comprehension

The keyword `as` is used to define the columns within the first line of a table comprehension.

```envision
table T = with
  [| as Column1, as Column2 |] // two columns defined
  [| "row 0",    42         |]
  [| "row 1",    43         |]
```

Table comprehensions are a mechanism offered by Envision to create tables without importing them from files.

## 'write (table) as (path) with', write block

The keyword `as` is used to specify the output path in a `write` block:

```envision
// Generate and write a file

table Products = with
  [| as Product, as Price |]
  [| "shirt", 10.50 |]
  [| "pants", 15.00 |]
  [| "hat", 5.25 |]

write Products as "/sample/products.csv" with
  Product = Products.Product
  Price = Products.Price
```

It can also be used with `partitioned` to write multiple files. The vector passed after the `as` must belong to an upstream table relative to the table being written.

```envision
// Generate and write multiple files

table Products = with
  [| as Product, as Price |]
  [| "shirt", 10.50 |]
  [| "pants", 15.00 |]
  [| "hat", 5.25 |]

// Compute ranks according to a unique grouping 'by 1'.
// Proceed with the whole 'Products' table with 'scan Products.Product'
Products.ProductIndex = rank() by 1 scan Products.Product

// table 'P' is upstream of 'Products'
table P[path] = by "/sample/products-\{Products.ProductIndex}.csv"

// Write each product to a separate file using 'partitioned'
write Products partitioned as path with
  Product = Products.Product
  Price = Products.Price
```

