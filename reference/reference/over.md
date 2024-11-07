+++
title = "over"
+++

## `over`, aggregator option

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
