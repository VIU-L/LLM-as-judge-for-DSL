+++
title = "in"
+++

## (T.'a in U.'a) 🡒 T.boolean, operator

The reserved keyword `in` is a binary operator returning `true` if the value found on the left vector exists anywhere in the right vector, and `false` otherwise.

Example:

```envision
table Products[product] = with
  [| as Product, as Price |]
  [| "apple",  1.25 |]
  [| "banana", 0.75 |]
 
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 8, 15), 3 |]
  [| "apple",  date(2020, 8, 16), 7 |]
  [| "orange", date(2020, 8, 16), 2 |]
 
where Orders.Pid in product // 'orange' is filtered out
  Orders.Amount = Orders.Quantity * Products.Price[Orders.Pid]
  show table "Orders" a1c3 with
    Orders.Pid
    Orders.OrderDate
    Orders.Amount
```

The `in` keyword can also be applied to tuples of vectors.

```envision
table T = with
  [| as A, as X, as Y, as Z |]
  [| "foo", 0, 1, 1 |]
  [| "bar", 1, 0, 0 |]

table U = with
  [| as X, as Y, as Z |]
  [| 0, 0, 0 |]
  [| 0, 1, 1 |]

where (T.X, T.Y, T.Z) in (U.X, U.Y, U.Z) // select the 'foo' line 
  show table "T" a1d2 with T.A, T.X, T.Y, T.Z
```
