+++
title = "partitioned"
+++

### partitioned, contextual keyword

The contextual keyword `partitioned` modifies the behavior of the `write` block: several files can be written at once.

```envision
table Products = with
  [| as Product, as Color, as Price |]
  [| "shirt", "white", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "white", 5.25 |]
 
Products.Path = "/sample/products-\{Products.Color}.csv"

write Products partitioned as Products.Path with
  Product = Products.Product
  Color = Products.Color
  Price = Products.Price
```

The script above can be rewritten with the introduction of a table that reifies the list of files to be written.

```envision
table Products = with
  [| as Product, as Color, as Price |]
  [| "shirt", "white", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "white", 5.25 |]

table P[path] = by "/sample/products-\{Products.Color}.csv"

write Products partitioned as path with
  Product = Products.Product
  Color = Products.Color
  Price = Products.Price
```

The maximum number of files that are allowed to be produced by a single `write .. partitioned` block is 100. Any attempt to produce more files will fail at runtime.

### See also

* [write](../../vwx/write/).
