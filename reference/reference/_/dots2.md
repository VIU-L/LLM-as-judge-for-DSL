+++
title = "(..) range operator"
+++

The double dot symbol (..) is a range operator intended to delimit a segment or a ray of values. The left and right boundaries, when present, are always inclusive.

## (..) range operator for `autodiff`

This operator delimits the acceptable values for parameters within an `autodiff` block:

```envision
table P = extend.range(3)
P.X = 5
 
autodiff Scalar epochs:1000 with
  params P.X in [P.N .. 42] // inclusive real-valued segment
  return sum(P.X)
 
show table "" a1b3 with P.N, P.X // P.X converges to 1, 2, 3
```

## (..) range operator for `loop`

This operator delimits the iterations within a `loop` block:

```envision
s = 0
loop n in 11 .. 15 // inclusive integer segment between 11 and 15
  s = s + n
show summary "" with s // 65
```

## (..) range operator for `match` (catch-all)

This operator delimits the matching patterns within a `match` block:

```envision
table T = with
  [| as Value |]
  [| -7       |]
  [| 0        |]
  [| 1        |]
  [| 3        |]
  [| 99       |]
 
T.Label = match T.Value with
  0       -> "Zero"
  .. 0    -> "Negative"
  1       -> "One"
  2 .. 10 -> "A few"
  ..      -> "Many" // catch-all
 
show table "Situations" a1c4 with
  T.Value
  T.Label
```

## (..) range operator for `over`

This operator delimits a segment introduced by `over` within a process:

```envision
table Orders = with
  [| as Product, as OrderDate, as Quantity |]
  [| "banana", date(2020, 4, 14), 5 |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]
  [| "banana", date(2020, 4, 17), 2 |]

Orders.Mavg = sum(Orders.Quantity)
  by Orders.Product
  over Orders.OrderDate = [-1 .. 0]

Orders.Cumul = sum(Orders.Quantity)
  by Orders.Product
  over Orders.OrderDate = [.. 0]

show table "" a1d10 with
  Orders.Product
  Orders.OrderDate
  Orders.Mavg  // Moving average over 2 days
  Orders.Cumul // Cumulative sum
```

## (..) range operator for `read`

This operator delimits a segment used to filter a file partition:

```envision
schema '/sample/products-\{Bucket}.csv' with
  Bucket : number
  Product : text
  Color : text
  Price : number

const lowerIncl = 1
const higherIncl = 2
read '/sample/products-\{lowerIncl..higherIncl}.csv' as Products

show table "My Products" a1d4 with
  Products.Bucket
  Products.Product
  Products.Color
  Products.Price
```

## (..) range operator for `span`

This operator delimits a continous date segment within a `span` block:

```envision
table Orders = with
  [| as OrderDate, as Quantity |]
  [| date(2021, 1, 2),   1 |]
  [| date(2021, 1, 3),   2 |]
  [| date(2021, 1, 5),   2 |]
  [| date(2021, 1, 5),   1 |]
  [| date(2021, 1, 9),   2 |]
  [| date(2021, 1, 12),  2 |]
  [| date(2021, 1, 17),  2 |]
  [| date(2021, 1, 17),  1 |]
 
span date = [min(Orders.OrderDate) .. max(Orders.OrderDate)]
  expect Orders.date = Orders.OrderDate
  Day.Quantity = sum(Orders.Quantity)
  show linechart "Daily Orders" a1c2 {seriesType: "stack"} with 
    Day.Quantity
```

## (..) range operator for `table`

This operator delimits the _warning_ segment for the size of the table.

```envision
table T max 1k..1m = extend.range(100)
```

The segment operates as follow:

* if the table size is less than below the lower bound, then no warning is emitted.
* if the table size in between the lower and upper bounds (inclusive), then a warning is emitted.
* if the table size is above the upper bound, then the script fails with an error.

## (..) range operator for `write`

This operator delimits a segment used to filter a file partition:

```envision
schema '/sample/products-\{Bucket}.csv' with
  Bucket : number
  Product : text
  Color : text
  Price : number

table Products = with
  [| as Product, as Color, as Price, as Bucket |]
  [| "shirt",    "white,grey", 10.50,       1 |]
  [| "pants",    "blue",       15.00,       2 |]

const lowerIncl = 1  // inclusive lower bound
const higherIncl = 2 // inclusive higher bound
write Products partitioned as '/sample/products-\{lowerIncl..higherIncl}.csv'
```
