+++
title = "where"
+++

The keyword `where` generally denotes a table being filtered in Envision.

## where (cond), where block

In a `where` block, the keyword `where` filters the specified table.

```envision
table T = with
  [| as N |]
  [| 0 |]
  [| 1 |]
  [| 2 |]
  [| 3 |]

where T.N mod 2 == 0 // where block
  // 2-space indent required inside the block
  T.Twice = 2 * T.N
  show table "filtered" a1b2 with T.N, T.Twice
```

The `Scalar` table cannot be filtered by `where`. Attempting to filter the `Scalar` table will fail at compile-time.

A `where` block cannot appear inside a `show` statement. Unlike SQL statements where the `WHERE` keyword appers after the `SELECT` keyword, in Envision, `where` appears before the `show` statement.

The `where` block is typically intended to keep the same filter(s) active while several operations happen.

The indent can be avoided by using the keyword `keep`:

```envision
table T = with
  [| as N |]
  [| 0 |]
  [| 1 |]
  [| 2 |]
  [| 3 |]

keep where T.N mod 2 == 0
// we are inside the 'where' block, but no indent due to 'keep'
T.Twice = 2 * T.N
show table "filtered" a1b2 with T.N, T.Twice
```

## .. = (expr) where (cond), filtered assignment

On the right side of an assignment, the keyword `where` filters the line being effectively assigned.

```envision
table Products = with // The table 'Products' has 3 lines
  [| as Product, as Price |]
  [| "cap",      3.50     |]
  [| "hat",      2.50     |]
  [| "ball",     4.00     |]

// This assignment is filtered by 'Products.Price < 3'
// Only the 'hat' line is modified
Products.Price = Products.Price * 1.1 where Products.Price < 3

// The 'hat' line has now a price of '2.75'
show table "" with Products.Product, Products.Price
```

This syntax is logically equivalent to the more verbose `where` block:

```envision
table Products = with
  [| as Product, as Price |]
  [| "cap",      3.50     |]
  [| "hat",      2.50     |]
  [| "ball",     4.00     |]

where Products.Price < 3
  Products.Price = Products.Price * 1.1 

show table "" with Products.Product, Products.Price
```

## table .. = where (cond), filtered table creation

In a table definition, the keyword `where` indicates the creation of a filtered table.

```envision
table Orders = with
  [| as MyId, as MyDate, as Quantity |]
  [| "A",  date(2023,1,5), 5 |]
  [| "A",  date(2023,1,11), 2 |]
  [| "B",  date(2023,1,20), 1 |]

// The table 'OnlyA' is filtered from 'Orders'.
// Original columns of 'Orders' are cloned into 'OnlyA'.
table OnlyA = where Orders.MyId == "A" 

// Broadcast from 'Orders' to 'OnlyA' is possible
OnlyA.Twice = 2 * Orders.Quantity

show table "A only" with OnlyA.MyId, OnlyA.MyDate, OnlyA.Twice 
```
