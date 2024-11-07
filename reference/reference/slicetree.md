+++
title = "slicetree"
+++

## slicetree, tile type

The `slicetree` is an interactive tile that offers navigation controls to pick a slice.

![Image](/images/ref_slicetree.png)

```envision
table P = with
  [| as Family, as Subfamily, as Product, as Price |]
  [| "Garment", "Clothing", "Pant",   25 |]
  [| "Garment", "Clothing", "Shirt",  15 |]
  [| "Garment", "Accessory", "Hat",   12 |]
  [| "Home", "Furniture", "Table",    75 |]
  [| "Home", "Accessory", "Tabletop",  7 |]

table Slices[slice] = slice by P.Product title: P.Product

Slices.Family = same(P.Family)
Slices.Subfamily = same(P.Subfamily)
Slices.Product = same(P.Product)

show slicetree "My tree selector" a1b4 with
  Slices.Family
  Slices.Subfamily
  Slices.Product

show table "Selected product" c1d4 slices:slice with
  P.Product
  P.Price
```

In the above script, the `slicetree` introduces a hierarchy with 3 levels.

The `slicetree` supports an arbitrary number of hierarchical levels. Each extra level comes as an extra text vector being added to the tile block. The tile gets a tuple _(level 1, level 2, .., level n)_ of text values obtained for each slice. Empty text values (i.e. `""`) are not allowed.

This tile creates a tree structure: a first level of nodes for each _(level 1)_ value, a second level of nodes for each _(level 1, level 2)_ value, and so on.

For every distinct tuple _(level 1, level 2, .., level n)_, the tile selects exactly one tile among all the slices that matche the tuple. If the `slice` dimension itself is (implicitely) used as the last level, then there is no ambiguity.

The `slicetree` tile offers the possibly to reorder the hierarchical levels through the `order by` tile option:

```envision
table P = with
  [| as Family, as FC, as Subfamily, as SC, as Product, as Price |]
  [| "Garment", 2,     "Clothing",  11,      "Pant",     25 |]
  [| "Garment", 2,     "Clothing",  11,      "Shirt",    15 |]
  [| "Garment", 2,     "Accessory", 12,      "Hat",      12 |]
  [| "Home",    1,     "Furniture", 13,      "Table",    75 |]
  [| "Home",    1,     "Accessory", 14,      "Tabletop",  7 |]

table Slices[slice] = slice by P.Product title: P.Product

Slices.Family = same(P.Family)
Slices.FC = same(P.FC)
Slices.Subfamily = same(P.Subfamily)
Slices.SC = same(P.SC)
Slices.Product = same(P.Product)

show slicetree "My tree selector" a1b4 with
  Slices.Family
  Slices.Subfamily
  Slices.Product
  order by [Slices.FC, Slices.SC, Slices.Product]

show table "Selected product" c1d4 slices:slice with
  P.Product
  P.Price
```

The ordering applies to the table `Slices` and must be consistent with the construction of the tree. In practice, specifying the ordering through a tuple aligned with the tree levels - as done in the above script - ensures the consistency of the ordering.
