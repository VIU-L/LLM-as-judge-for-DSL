+++
title = "piechart"
+++

## piechart, tile type

The `piechart` tile is intended to display a piechart. The tile expects one vector passed as argument and one `group by` option.

```envision
table T = with 
  [| as Product, as Country |]
  [| "Shirt",   "FR"        |]
  [| "Hat",     "FR"        |]
  [| "Hat",     "US"        |]
  [| "Pant",    "US"        |]
  [| "Pant",    "UK"        |]
  [| "Shoes",   "UK"        |]

T.Sales = random.poisson(10 into T)

show piechart "Sales per product" a1c6 {unit: "$"} with
  sum(T.Sales)
  group by T.Product
```

The aggregator is not needed if `group by` is done with a dimension.

```envision
table T[product] = with 
  [| as Product |]
  [| "Shirt"    |]
  [| "Hat"      |]
  [| "Pant"     |]
  [| "Shoes"    |]

T.Sales = random.poisson(10 into T)

show piechart "Sales per product" a1c6 {unit: "$"} with
  T.Sales
  group by product
```
