+++
title = "span"
+++

## span, keyword

The `span` keyword is used to unfilter the calendar dimensions.

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
