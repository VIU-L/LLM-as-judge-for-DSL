+++
title = "group"
+++

The keyword `group` is used always used as `group by` within a tile block in Envision.

## 'show .. with .. group by expr', grouping at the tile-level

The `group by` option is similar to a `by` grouping, but applied to the whole tile-block.

```envision
table C = with
  [| as Country, as Region,       as UnitSold, as InEuros |]
  [| "France",   "Europe",        100,         10000      |]
  [| "Germany",  "Europe",        125,         12500      |]
  [| "USA",      "North America", 1000,        100000     |]
  [| "Canada",   "North America", 75,          7500       |]

show table "Units per Region" with
  sum(C.UnitSold) as "Units" // implicit 'by C.Region'
  sum(C.InEuros) as "€"      // implicit 'by C.Region'
  group by C.Region
// Units,€
// 225,22500
// 1075,107500
```

The `group by` is a syntactic sugar for:

```envision
table C = with
  [| as Country, as Region,       as UnitSold, as InEuros |]
  [| "France",   "Europe",        100,         10000      |]
  [| "Germany",  "Europe",        125,         12500      |]
  [| "USA",      "North America", 1000,        100000     |]
  [| "Canada",   "North America", 75,          7500       |]

table Regions = by C.Region // table 'Regions' is upstream of table 'C' 

show table "Units per Region" with
  sum(C.UnitSold) into Regions as "Units" // aggregate into an upstream table
  sum(C.InEuros) into Regions as "€"      // idem
```
