+++
title = "[] lookup operator"
+++

The lookup operator `[..]` is used to request a value a vector by specifying a key that belongs to the primary dimension of the probed table.

```envision
table Products[product] = with
  [| as Product,   as Price |]
  [| "apple",      1.50     |]
  [| "pear",       1.30     |]
  [| "orange",     2.10     |]
  [| "clementine", 2.70     |]
 
table Selection = with
  [| as Choice |]
  [| "pear"    |]
  [| "orange"  |]
  [| "banana"  |] // missing

Selection.PriceOfSelection = Products.Price[Selection.Choice] // lookup operator

show table "Selection" a1b4 with
  Selection.Choice
  Selection.PriceOfSelection as "Price"
```

When trying to access a missing key, the lookup operator returns the default value for the datatype:

```envision
table Products[product] = with
  [| as Product,   as Price |]
  [| "apple",      1.50     |]
  [| "pear",       1.30     |]
  [| "orange",     2.10     |]
  [| "clementine", 2.70     |]
 
missingPrice = Products.Price["banana"] // 0 (default number value)

show scalar "" with missingPrice // 0
```

It is possible to force a runtime failure:

```envision
table Products[product] = with
  [| as Product,   as Price |]
  [| "apple",      1.50     |]
  [| "pear",       1.30     |]
  [| "orange",     2.10     |]
  [| "clementine", 2.70     |]
 
missingPrice = Products.Price["banana"] default fail // 'Key not found in lookup.' (runtime error)

show scalar "" with missingPrice // never displayed
```

Or specify an explicit default value:

```envision
table Products[product] = with
  [| as Product,   as Price |]
  [| "apple",      1.50     |]
  [| "pear",       1.30     |]
  [| "orange",     2.10     |]
  [| "clementine", 2.70     |]
 
missingPrice = Products.Price["banana"] default -1 // -1 when missing

show scalar "" with missingPrice // -1
```
