+++
title = "Read dimensions"
description = ""
weight = 2
+++

Storing tables in files is convenient but unlike storing data in a relational database, structured relations between tables are not a given and integrity problems may arise. For example, nothing prevents a flat text file from containing duplicated lines. Thus, Envision offers a mechanism to add _relational structure_ to a set of tables being read as inputs. Those mechanisms are not only desirable from a correctness perspective, as it prevents certain classes of problems from happening in the first place (e.g. having a sales order referencing a non-existent product), but they are also desirable thanks to the built-in behaviors that Envision offers when those relations are declared.

Let’s revisit the example from the previous section considering two tables `Products` and `Variants`. Each variant is supposed to be attached to a product, and can only vary in color compared to the original product. The following script illustrates how to generates two CSV files, one for the products and the other for the variants:

```envision
table Products = with
  [| as Product, as Price |]
  [| "shirt", 10.50 |]
  [| "pants", 15.00 |]
  [| "hat", 5.25 |]

table Variants = with
  [| as Product, as Color |]
  [| "shirt", "white" |]
  [| "shirt", "pink" |]
  [| "pants", "blue" |]
  [| "pants", "black" |]
  [| "hat", "red" |]

write Products as "/sample/products.csv" with
  Product = Products.Product
  Price = Products.Price

write Variants as "/sample/variants.csv" with
  Product = Variants.Product
  Color = Variants.Color
```

The following script reads both files, and loads two tables `Products` and `Variants` and then displays the number of available colors, among the variants, for every product:

```envision
read "/sample/products.csv" as Products[product] with
  "Product" as product : text
  Price : number

read "/sample/variants.csv" as Variants expect [product] with
  "Product" as product : text
  Color : text

Products.Colors = distinct(Variants.Color)

show table "Color Counts" a1b3 with
  product
  Products.Colors
```

The script above starts by declaring `product` as the _primary dimension_ of the table `Products`. The primary dimension is introduced between brackets right after the table name. As the name of the dimension matches (case-insensitive) the name of one of the file’s input columns, namely `Product: text` below, this column is used as the primary dimension. If duplicates were to be found in the `Product` column, the read operation would fail at runtime indicating that the unicity constraint of the primary dimension has been violated.

<!-- [vermorel] 2020-07 TODO: not working yet, see https://lokad.atlassian.net/browse/LK-6566 -->

The table `Variants` is declared with `product` as a foreign dimension. This declaration follows the `expect` keyword (itself following the table name), and the name of the referenced dimension is put between brackets. If values were to be found in the `Variants.Product` column without having a counterpart in the `product` dimension, the read operation would fail indicating that the foreign dimension constraint has been violated.

Thus, if both read operations succeed, Envision guarantees that the table `Products` has no duplicates for `Products.Product`, and that every single line in `Variants` has exactly one counter line in the `Products` table. This latter property can be rephrased in a more Envision-esque perspective: due to the foreign dimension, the table `Products` can be broadcast into the table `Variants`.

This broadcast retaliationship makes it possible to define `Products.Colors` as done above by leveraging the natural join that exists between the two tables. Indeed, for every single of the `Products` table, we can identify without ambiguity the matching lines in the `Variants` table through the pairs `Products.Product` and `Variants.Product`.

If we had omitted the dimension declarations, it would have remained possible to produce a similar effect with:

```envision
read "/sample/products.csv" as Products with
  Product : text
  Price : number

read "/sample/variants.csv" as Variants with
  Product : text
  Color : text

Products.Colors = distinct(Variants.Color) by Variants.Product at Products.Product

show table "Color Counts" a1b3 with
  Products.Product
  Products.Colors
```

In the script above, the explicit `by at` aggregation option tells Envision how to pair the lines in the two tables `Products` and `Variants`.

As a rule of thumb, it’s better to declare dimension relationships to the greatest extent through the `read` statements rather than to rely on the `by at` options. Not only does Envision have built-in integrity checks, but the code tends to be more concise and more readable, especially when the pairing ends-up being repeated numerous times in the script.

Multiple dimensions can also be referenced. Let’s revisit the script introduced above with a third table named `Colors` exported to a third file as well with:

```envision
table Products = with
  [| as Product, as Price |]
  [| "shirt", 10.50 |]
  [| "pants", 15.00 |]
  [| "hat", 5.25 |]

table Colors = with
  [| as Color |]
  [| "black" |]
  [| "blue" |]
  [| "pink" |]
  [| "white" |]

table Variants = with
  [| as Product, as Color |]
  [| "shirt", "white" |]
  [| "shirt", "pink" |]
  [| "pants", "blue" |]
  [| "pants", "black" |]
  [| "hat", "red" |]

write Products as "/sample/products.csv" with
  Product = Products.Product
  Price = Products.Price

write Colors as "/sample/colors.csv" with
  Color = Colors.Color

write Variants as "/sample/variants.csv" with
  Product = Variants.Product
  Color = Variants.Color
```

These three files can be loaded with with the following script:

```envision
read "/sample/products.csv" as Products[product] with
  "Product" as product : text
  Price : number

read "/sample/colors.csv" as Colors[color] with
  "Color" as color : text

read "/sample/variants.csv" as Variants expect [product, color] with
  "Product" as product : text
  "Color" as color : text

Products.Colors = distinct(Variants.color)
Colors.Products = distinct(Variants.product)

show table "Color per Product" a1b3 with
  product
  Products.Colors

show table "Product per Color" c1d3 with
  color
  Colors.Products
```

The tables `Products` and `Colors` both declare a primary dimension, `product` and `color`. The table `Variants` declare those two dimensions as foreign dimensions, using the comma (`,`) as the delimiter within the brackets `[` and `]`. The `Variants` table benefits from two natural joins, illustrated by the respective definitions of `Products.Color` - counting the number of distinct colors for every product - and of `Colors.Products` - counting the number of distinct products for every color.

Any arbitrary number of foreign dimensions can be declared after the `expect` keyword following the syntax `[dim1, dim2, dim3, ..]`. Every referenced dimension generates a broadcast relationship between the two tables, and also ensures - at runtime - that all the values are found in their corresponding matching dimension.

The declarations of the primary dimensions must precede any use of the same dimension as a secondary dimension.

<!-- [vermorel] 2020-07 TODO: Clarify that primary dimension and expect should only be specified in the first statement. Not implemented yet. See https://lokad.atlassian.net/browse/LK-6588 -->

As a final note on dimensions, it is also possible to declare a primary dimension that does not match any of the columns declared by the `read` statement.

```envision
read "/sample/products.csv" as Products[id] with
  Product : text
  Price : number
```

The primary dimension `id` does not match any column, and ends up being automatically generated with one unique identifier per line in the original file. The datatype of `id` is `ordinal`, which is an intentionally opaque type that does not offer much by way of syntax in Envision.
