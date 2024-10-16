+++
title = "Secondary dimensions"
description = ""
weight = 5
+++

Dimensions characterize the relational structure of the tables processed by Envision. With the proper dimensions in place between the tables of interest, most operations can be performed with little syntactic overhead. This approach differs from the more traditional approach taken by query languages, like SQL, which emphasize explicit joins.

In Envision, broadcasts and aggregations derives from the presence of dimensions. A table can be broadcast into all its downstream tables. A table can be aggregated into all its upstream table. Below, we do not revisit those operations. Instead, we strictly focus on the dimensions which allow them in the first place.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Primary and secondary dimensions

Each table has one, and only one, primary dimension. The table can be seen as a “container” of vectors, while the primary dimension can be seen as the “shared structure” that is backing every vector. The primary dimension is frequently implicit:

```envision
table Colors = with
  [| as Color |]
  [| "red"    |]
  [| "blue"   |]
  [| "green"  |]

show table "Colors" a1a3 with Colors.Color
```

In the above script, the primary dimension of the table `Colors` exists but remains implicit. This dimension can be named:

```envision
table Colors[c] = with
  [| as Color |]
  [| "red"    |]
  [| "blue"   |]
  [| "green"  |]

show table "Colors" a1a3 with Colors.Color
```

In the above script, the primary dimension is named `c`. It is auto-generated with the type `ordinal`.

The `ordinal` type has some uses in Envision, but these are for relatively fringe cases. In practice, when explicitly naming a primary dimension, it is also of interest to have this vector explicitly constructed as well:

```envision
table Colors[color] = with
  [| as color |]
  [| "red"    |]
  [| "blue"   |]
  [| "green"  |]

show table "Colors" a1a3 with color
```

In the above script, as the name of the primary dimension `color` associated with the declaration of the table `Colors` matches the name of one of the input vectors, this matching vector becomes the primary dimension itself.

Let’s point out that not all vectors can become a primary dimension: values have to be distinct, or the creation of the primary dimension fails at runtime, as illustrated by:

```envision
table Colors[color] = with
  [| as color |]
  [| "red"    |]
  [| "blue"   |]
  [| "green"  |]
  [| "green"  |] // WRONG! Duplicate!

show table "Colors" a1a3 with color
```

A secondary dimension is a vector that only contains values originating from a known primary dimension. The secondary dimension is found in a table that differs from the table originally associated with the primary dimension. Let’s refer to those two tables as the primary table and secondary table. The concept of secondary dimension comes with one central property: when a secondary dimension is present, every line of the secondary table has exactly one corresponding line in the primary table.

The simplest way to add a secondary dimension consists of directly leveraging a (primary) dimension to construct one of its vectors:

```envision
table Colors[color] = with
  [| as color |]
  [| "red"    |]
  [| "blue"   |]
  [| "green"  |]

table Products = with
  [| as Label, as color |]
  [| "Hat",    color    |]
  [| "Shirt",  color    |]

where Colors.color == "red" // 2 lines displayed
  show table "Products" a1b6 with Products.Label, Products.color
```

In the above script, the vector `Products.color` is directly constructed through `color` - the primary dimension of the table `Colors`. As a result, the table `Products` gets `color` as a secondary dimension. The presence of this secondary dimension within the table `Products` is demonstrated by the impact of the `where` filter applied to the table `Colors`, which triggers a secondary filter on the `Products` table.

In the Envision terminology, the table that contains the secondary dimension is referred to as being _downstream_ of the table that contains the primary dimension. Conversely, the table that contains the primary dimension is referred to as being _upstream_ of the table that contains the secondary dimension. These concepts of upstream and downstream play an important role in the mechanics involved with the `each` blocks, which will be introduced later.

Once a name has been given to a primary dimension, that named is reserved to represent that dimension across all tables, and any existing columns with that name become hidden and inaccessible:

```envision
table Products = with
  [| as Label, as color |]
  [| "Hat",    "red"    |]
  [| "Shirt",  "blue"   |]

table Colors[color] = with
  [| as color |]
  [| "red"    |]
  [| "blue"   |]
  [| "green"  |]

show table "Products" a1b6 with 
  Products.Label
  Products.color // WRONG! Dimension 'color' not present in table 'Products'.
```

In the above example, the statement `table Colors[color]` defines a new primary dimension `color`. From that point on, the name `color` used in other tables will represent a secondary dimension instead of a named column: in the case of `Products.color`, the reference fails because a second dimension `color` is not present in table `Products`, and the existing column named `color` can no longer be accessed.

Conversely, when creating a secondary dimension, the name must match that of the primary dimension, otherwise, a vector is created based on the values found in the primary dimension but without enforcing the newly created vector as being a secondary dimension:

```envision
table Colors[color] = with
  [| as color |]
  [| "red"    |]
  [| "blue"   |]
  [| "green"  |]

table Products = with
  [| as Label, as Variant |]
  [| "Hat",    color      |]
  [| "Shirt",  color      |]

where Colors.color == "red" // 6 lines displayed
  show table "Products" a1b6 with Products.Label, Products.Variant
```

In the above script, the `where` filter applied to `Colors` has no effect on `Products`. The vector `Products.Variant` is merely a vector of type `text`. The values of this vector originate from the vector `Colors.color` (which could also be more concisely written as `color`) but the dimensional aspect is ignored.

## Filtering and dimensions

Filtering is a mechanism in Envision that creates a table out of a pre-existing table. Filtering preserves dimensions, primary or secondary, if any, as secondary dimensions:

```envision
table Colors[color] = with
  [| as Color, as Code |]
  [| "red",    0       |]
  [| "blue",   1       |]
  [| "green",  2       |]

table Products = with // 6 lines
  [| as Label, as color |]
  [| "Hat",    color    |]
  [| "Shirt",  color    |]

table FewProducts = where not (Products.Label == "Hat" and color == "red")

FewProducts.Label = Products.Label
FewProducts.ColorCode = Colors.Code // 'color' as secondary dimension

show table "Some products" with FewProducts.Label, FewProducts.ColorCode
```

In the above script, the table `Products` has `color` as a secondary dimension. The table `FewProducts` inherits this secondary dimension as a secondary dimension of its own via the table creation mechanism `table FewProducts = where ..`.

Similarly, a primary dimension can also be inherited, but it will be inherited as a secondary dimension instead of a primary one:

```envision
table Colors[color] = with
  [| as Color, as Code |]
  [| "red",    0       |]
  [| "blue",   1       |]
  [| "green",  2       |]

table FewColors = where color != "red"

FewColors.Code = Colors.Code

show table "Some products" with FewColors.Code
```

In the above script, the table `Colors` has `color` as its primary dimension. The table `FewColors` inherits `color` as a secondary dimension via the same table creation mechanism.

## Adding a secondary dimension

As secondary dimensions are pivotal in Envision to express operations across multiple tables without resorting to explicit joins, Envision offers a short series of mechanisms to add a secondary dimension to a table, namely:

* A compile-time mechanism, `T.dim = U.dim`
* A safe runtime mechanism, `where T.dim = expr`
* A guarded runtime mechanism, `expect T.dim = expr`

Those mechanisms have in common that, once the name `dim` has been given to a dimension, a vector `T.dim` can only exist if it represents that dimension in the table `T`. Furthermore, no value can be assigned to `T.dim` outside the three mechanisms listed in this section to add a secondary dimension to the table `T`.

### Safe at compile time

A secondary dimension can be added at compile time when the Envision compiler can prove that the operation is correct. The situations where such a proof can be obtained without obtaining the dimension _by design_ through the construction of the table itself are somewhat rare. Such a situation occurs with cross tables (cross tables will be detailed later on):

```envision
table Colors[color] = with
  [| as Color, as Code |]
  [| "red",    0       |]
  [| "blue",   1       |]
  [| "green",  2       |]

table Products = with // 6 lines
  [| as Label, as color |]
  [| "Hat",    color    |]
  [| "Shirt",  color    |]

table Locations = with
  [| as City    |]
  [| "New York" |]
  [| "Paris"    |]

table SKUs = cross(Locations, Products) // 12 lines

SKUs.color = Products.color // 'color' dimension added to 'SKUs'
SKUs.ColorCode = Colors.Code

show table "SKUs" with Locations.City, Products.Label, SKUs.ColorCode
```

In the above script, the table `SKUs` is a Cartesian product between `Locations` and `Products`. The table `SKUs` is referred to as a cross table and it does not automatically inherit the secondary dimensions from its source tables. However, `color`, which is already a secondary dimension of `Products`, is declared as a secondary dimension of `SKUs` via the assignment `SKUs.color = Products.color`.

The syntax `U.dim = T.dim`, where `dim` is a dimension, represents a special type of assignment which goes being the simple broadcast: the dimension `dim` becomes a secondary dimension of the table `U`. However, let’s immediately point out that in the general case, the Envision compiler cannot prove that such an assignment is correct. Thus, unless there are some special circumstances that make this proof possible, as illustrated by the cross table case above, such an assignment typically results in a compilation error.

### Safe at runtime

A secondary dimension can be added at runtime while performing a filtering operation at the same time. The purpose of the filter is to remove all the values that do not match the dimension. Thus, by construction, whatever passes through the filter, possibly nothing, offers a proper secondary dimension:

```envision
table Colors[color] = with
  [| as Color, as Code |]
  [| "red",    0       |]
  [| "blue",   1       |]
  [| "green",  2       |]

table Products = with 
  [| as Label, as Col  |]
  [| "Hat",    "red"   |]
  [| "Shirt",  "blue"  |]
  [| "Shirt",  "white" |]

where Products.color = Products.Col
  show table "Products" a1b3 with Products.Label, Colors.Code // 2 lines
```

In the above script, the statement `where Products.color = Products.Col` is both a filter and an addition of a secondary dimension to the table `Products`. With `color` as a secondary dimension, it becomes possible to broadcast from `Colors` into `Products`, which happens in the display of the `table` tile.

The syntax `where T.dim = expr` requires `dim` to be a named primary dimension. Assuming that the expression on the right side of the assignment has the correct type and that the expression does broadcast into the table `T`, the operation always succeeds, no matter whether the expression returns values matching those of `dim` or not. If zero matches are found then the table `T` is empty within the `where` block.

### Guarded at runtime

A secondary dimension can be added at runtime on the premise that values will be valid dimension-wise and suffer an execution failure otherwise:

```envision
table Colors[color] = with
  [| as Color, as Code |]
  [| "red",    0       |]
  [| "blue",   1       |]
  [| "green",  2       |]

table Products = with 
  [| as Label, as Col  |]
  [| "Hat",    "red"   |]
  [| "Shirt",  "blue"  |]
  [| "Shirt",  "red"   |]

expect Products.color = Products.Col

show table "Products" a1b3 with Products.Label, Colors.Code
```

In the above script, the statement `expect Products.color = Products.Col` is more than a simple vector assignment: the dimension `color` is added as a secondary dimension to the table `Products`. The values found in `Products.Col` are matched with those found in the vector `color`. If a value found in `Products.Col` cannot be found in `color`, then the execution fails.

The syntax `expect T.dim = expr` also requires `dim` to be a named primary dimension. Unlike the `where T.dim = expr` mechanism, this mechanism can fail. The mechanism is referred to as _guarded_ because this syntax still offers a certain degree of correctness: a successful execution of the script occurs if, and only if, the values of the expression do match the values of the dimension.
