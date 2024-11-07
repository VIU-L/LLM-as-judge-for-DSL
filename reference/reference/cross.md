+++
title = "cross"
+++

## cross, table creation

The `cross` keyword creates a table as the cartesian product of two tables. The resulting table has two primary dimensions, obtained from the primary dimensions of the left and right tables respectively.

```envision
table Products[product] = with
  [| as Product, as Price |]
  [| "shirt",  11.25 |]
  [| "pant",   25.75 |]
  [| "cap",     5.75 |]

table Colors[color] = with
  [| as Color |]
  [| "white" |]
  [| "black" |]
  [| "blue"  |]
  [| "red"   |]

table Variants = cross(Products, Colors)

show table "All variants" a1c10 with
  Variants.product
  Variants.color
  Products.Price
```

_Advanced remark_: In SQL, this mechanism is known as a cartesian join.

## cross by at, table creation
<!-- The by-at argument should become symmetrical
https://lokad.atlassian.net/browse/LK-10878 -->

The cross-by-at creates a table as the series of cartesian products from the two tables, with one cartesian product per group. The primary dimension of the new table is the concatenation of the primary dimensions of the left and right tables.

```envision
table T = with
  [| as A, as B |]
  [| "a",  1 |]
  [| "b",  1 |]
  [| "c",  2 |]
  [| "d",  2 |]

table U = with
  [| as B, as C |]
  [| 1, "x" |]
  [| 1, "y" |]
  [| 2, "z" |]

table TU = cross(T, U) by U.B at T.B
TU.A = T.A
TU.C = U.C

show table "TU" a1b10 with
  TU.A
  TU.C
```

_Advanced remark_: In SQL, this mechanism is known as an inner join.
