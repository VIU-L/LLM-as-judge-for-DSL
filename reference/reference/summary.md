+++
title = "summary"
+++

## summary, tile type

The `summary` tile is intended to gather a list of scalar values, typically KPIs.

```envision
myDate = date(2022, 2, 17)
onHand = 123
onOrder = 42
unitPrice = 25

show summary "Key figures" a1b2 with
  "Contoso A-001" as "Product Name"
  myDate
  onHand
  onOrder
  onHand + onOrder as "Total units" 
  (onHand + onOrder) * unitPrice as "Total value" {unit: "$"}
```

Each value can be associated to a label and a unit.
