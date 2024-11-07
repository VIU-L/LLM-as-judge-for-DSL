+++
title = "show"
+++

The keyword `show` introduces a tile to be displayed in Envision.

## 'show', display a tile

A dashboard produced by Envision is made of tiles. Below, a short selection of common tiles.

```envision
table C = with
  [| as Country, as Region,       as UnitSold, as InEuros |]
  [| "France",   "Europe",        100,         10000      |]
  [| "Germany",  "Europe",        125,         12500      |]
  [| "USA",      "North America", 1000,        100000     |]
  [| "Canada",   "North America", 75,          7500       |]

// Inline syntax
show label "Hello, World!"
show scalar "My number" with 123
show scalar "My text" with "hello"
show summary "Several scalar values" with 123, "hello", date(2024, 1, 31)

// Multiline syntax
show table "Sales by Region (table)" with
  C.Region
  sum(C.UnitSold) as "Units"
  sum(C.InEuros) as "€"
  group by C.Region

show barchart "Sales by Region (barchart)" with
  sum(C.InEuros) as "€"
  group by C.Region // populate the labels

show piechart "Sales by Region (piechart)" with
  sum(C.InEuros) as "€"
  group by C.Region
```
