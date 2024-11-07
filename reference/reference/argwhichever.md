+++
title = "argwhichever"
+++

## argwhichever(), aggregator

Returns true for one value of the group.

Example:

```envision
table Products = with
  [| as Label, as UnitPrice |]
  [| "Hat",    15.00        |]
  [| "Shirt",  15.00        |]
  [| "Pants",  25.00        |]

Products.IsTrue = argwhichever() by Products.UnitPrice

show table "" a1c3 with
  Products.Label
  Products.UnitPrice
  Products.IsTrue
```

## argwhichever(T.a: boolean), aggregator

Returns true for a value of the group for which the condition is true.

```envision
table Products = with
  [| as Label, as UnitPrice, as Eligible |]
  [| "Hat",    15.00,        false       |]
  [| "Shirt",  15.00,        true        |]
  [| "Pants",  25.00,        true        |]

Products.IsTrue = argwhichever(Products.Eligible) by Products.UnitPrice

show table "" a1c3 with
  Products.Label
  Products.UnitPrice
  Products.IsTrue
```
