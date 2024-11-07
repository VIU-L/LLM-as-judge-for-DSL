+++
title = "write"
+++

### wrike, keyword

The keyword `write` introduces a block used to define a section of vectors, associated to a given table, to be persisted as a flat file.

```envision
table Products = with
  [| as Product, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]
 
write Products as "/sample/products.csv" with
  Product = Products.Product
  Color = Products.Color
  Price = if Products.Price > 0 then Products.Price else 100
```

### See also

* [partitioned](../../pqr/partitioned/)
* [read](../../pqr/read/)
