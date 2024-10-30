+++
title = "Table comprehensions"
description = ""
weight = 7
+++

The table comprehension is a general mechanism supported by Envision to create tables from other tables and literals. Many of the script examples introduced so far leverage a simple hard-coded table, which is the simplest form of table comprehension. However, this form is only scratching the surface of what the table comprehension mechanism can do.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Syntax overview

Let's manually create a table as illustrated by:

```envision
table Colors = with
  [| as French, as English |] // This line is called a ‘Header’.
  [| "Rouge", "Red"  |]       // This line is called a ‘Yield’.
  [| "Bleu", "Blue"  |]
  [| "Vert", "Green" |]

show table "Colors" with Colors.French, Colors.English
```

Which displays the following table:

| French | English |
|--------|---------|
| Rouge  | Red     |
| Bleu   | Blue    |
| Vert   | Green   |

The script above illustrates the creation of a simple table named `Colors` based on hard-coded text literals. The comprehension has one header line and three yield lines.

A table comprehension begins with the `with` keyword and starts a _block scope_. Thus, both the header and the yields that follow require an extra level of indentation. The syntax of the table comprehension is closely related to the syntax of the return block. However, as soon as a header or a yield is introduced, Envision forbids the usage of a `return` statement. The number of yield lines is limited to 100. Displaying tiles with `show` statements is also not allowed within a comprehension block. Finally, as we will see in the following, the scoping rules of the return block also apply to the table comprehension.

_Advanced remark_: Design-wise, table comprehensions in Envision are the cousins of generator functions in Python used to return iterators, and also the cousins of comprehensions in Python (but also of F#, Haskell, etc.). Technically, it’s a particular case of _coroutine_, that is, functions that can be paused and resumed. This iterator flavor of coroutines is popular among many programming languages (C#, F#, Kotlin, etc). Table comprehensions are slightly more complex than usual iterators because the object returned - a table - is itself more complex than a plain object.

## Non-scalar values

The table comprehension offers the capability to compose a table from pre-existing tables. The primary use case in Envision of table comprehension is not to be handy when writing documentation materials with tiny hard-coded tables, but to offer a _tabular_ composition mechanism (the _columnar_ composition mechanism is a given through simple assignments). Let’s review a situation where a list of products is composed from two suppliers’ product lists:

```envision
table SupplierA = with
  [| as Product |]
  [| "banana"   |]
  [| "orange"   |]
  [| "peach"    |]

table SupplierB = with
  [| as Product |]
  [| "apple"    |]
  [| "banana"   |]

table Products = with
  [| as Product, as Supplier |]
  [| SupplierA.Product, "A" |]
  [| SupplierB.Product, "B" |]

show table "Products" with Products.Product, Products.Supplier
```

Which displays the following table:

| Product | Supplier |
|---------|----------|
| banana  | A        |
| orange  | A        |
| peach   | A        |
| apple   | B        |
| banana  | B        |

In the above script, the vectors `SupplierA.Product`  and `SupplierB.Product` are used within two separate yields. The vector `SupplierA.Product` adds 3 lines to the `Products` table, while the vector `SupplierB.Product` adds 2 lines.

In practice, a table comprehension is handy when it comes to consolidating distinct data sources into a single one, this can happen when the sales data is found both in the ecommerce platform and in the retail POS system for example.

It is also possible to interleave scalar and non-scalar values among the table yields. For example, the following script adds a _Total_ line at the end of a table that lists the unit sold per product:

```envision
table Products = with
  [| as Product, as Sold |]
  [| "apple", 4  |]
  [| "banana", 2 |]
  [| "orange", 7 |]

table WithTotal = with
  [| Products.Product as Product, Products.Sold as Sold |]
  [| "Total", sum(Products.Sold) by 1 |]

show table "Products with total" with
  WithTotal.Product
  WithTotal.Sold
```

Which displays the following table:

| Product | Sold |
|---------|------|
| apple   | 4    |
| banana  | 2    |
| orange  | 7    |
| Total   | 13   |

The above script interleaves a nonscalar yield aligned with the `Product` table and a scalar yield that leverages a scalar aggregation expression `sum(Products.Sold) by 1` (cf. the section “Scalar aggregation” above for the `by 1` shorthand).

Let’s point out that in the very specific case where one would seek to add a _total_ line at the end of a table, Envision provides a better mechanism than table comprehension through the use of StyleCode, which we will detail in the following. Indeed, having totals on the last line is typically a matter of _display_. If someone were to download the spreadsheet exported from the `table` tile, this person would most likely prefer _not_ to have the spreadsheet polluted by a heterogeneous last line. However this example does have the benefit of simplicity, which is why it is adopted in this section.

## Comprehension block

The table comprehension leverages a (syntax) block in Envision introduced by the keyword `with`. This block allows arbitrary assignments to be made, it is _not_ restricted to a header and yields. For example, we can revisit the last script of the previous section, and isolate the aggregation of the total number of units sold with:

```envision
table Products = with
  [| as Product, as Sold |]
  [| "apple", 4  |]
  [| "banana", 2 |]
  [| "orange", 7 |]

table WithTotal = with
  total = sum(Products.Sold)
  [| Products.Product as Product, Products.Sold as Sold |]
  [| "Total", total |]

show table "Products with total" with
  WithTotal.Product
  WithTotal.Sold
```

The script above is strictly identical to the last one of the previous section and displays the same table. The scalar aggregation `sum(Products.Sold)` is isolated at the beginning of the block through the assignment of the `total` variable. This variable is later used as part of the final yield.

Let’s immediately point out that assignments can be freely interleaved with the comprehension itself, for example the following script is also valid:

```envision
table Products = with
  [| as Product, as Sold |]
  [| "apple", 4  |]
  [| "banana", 2 |]
  [| "orange", 7 |]

table WithTotal = with
  total = sum(Products.Sold)
  [| Products.Product as Product, Products.Sold as Sold |]
  copy = total
  [| "Total", copy |]

show table "Products with total" with
  WithTotal.Product
  WithTotal.Sold
```

The script aboves interleaves the assignment `copy = total` between the two yields to illustrate that the comprehension block behaves (mostly) like a regular block of Envision code, putting aside the display of tiles and `return` statements.

Then, as with the return block, the variables that are introduced within the `with` block are _block scoped_. This implies that those variables cannot be used any more once the block has been exited. The following faulty script illustrates this behavior:

```envision
table Products = with
  [| as Product, as Sold |]
  [| "apple", 4  |]
  [| "banana", 2 |]
  [| "orange", 7 |]

table WithTotal = with
  total = sum(Products.Sold)
  [| Products.Product as Product, Products.Sold as Sold |]
  [| "Total", total |]

show label "\{total}" // WRONG! Undefined variable 'Scalar.total'.
```

This script gives a compilation error `Undefined variable 'Scalar.total'` which is precisely what we expected, as the last line attempts to access the variable `total` outside of its scope.

## Filtered yields

Within a table comprehension, `where` (i.e. filter) blocks are allowed. Filtering grants a more fine-grained control on the resulting table’s content. For example we can revisit our two suppliers example above with:

```envision
table SupplierA = with
  [| as Product |]
  [| "banana"   |]
  [| "orange"   |]

table SupplierB = with
  [| as Product |]
  [| "apple"    |]
  [| "banana"   |]

table Products = with
  where SupplierA.Product != "banana"
  where SupplierB.Product != "banana"
    [| as Product, as Supplier |]
    [| SupplierA.Product, "A" |]
    [| SupplierB.Product, "B" |]

show table "Products" with Products.Product, Products.Supplier
```

Which now displays the reduced table:

| Product | Supplier |
|---------|----------|
| orange  | A        |
| apple   | B        |

However, there are not specific restrictions concerning the placement of the filters. The `where` blocks can be interleaved with header and yields. Thus, the above script can be rewritten under a slightly different form that still displays the same table:

```envision
table SupplierA = with
  [| as Product |]
  [| "banana"   |]
  [| "orange"   |]

table SupplierB = with
  [| as Product |]
  [| "apple"    |]
  [| "banana"   |]

table Products = with
  [| as Product, as Supplier |]
  where SupplierA.Product != "banana"
    [| SupplierA.Product, "A" |]
  where SupplierB.Product != "banana"
    [| SupplierB.Product, "B" |]

show table "Products" with Products.Product, Products.Supplier
```

Finally, external filters outside the table comprehension still apply as well. Thus, it is possible to rewrite the above script into yet another form that still displays the same table:

```envision
table SupplierA = with
  [| as Product |]
  [| "banana"   |]
  [| "orange"   |]

table SupplierB = with
  [| as Product |]
  [| "apple"    |]
  [| "banana"   |]

where SupplierA.Product != "banana"
where SupplierB.Product != "banana"
  table Products = with
    [| as Product, as Supplier |]
    [| SupplierA.Product, "A" |]
    [| SupplierB.Product, "B" |]

show table "Products" with Products.Product, Products.Supplier
```

As a rule of thumb, if the filters are only used to filter the yields, then it’s clearer to keep the `where` blocks _inside_ the table comprehension as illustrated by the very first script in this section. Performance-wise, the placement of the filter has no consequence, but placing the filter outside the table comprehension could mistakenly hint that that filtering something else beyond the table comprehension was intended.

## Multiline yields

Within a table comprehension, the multiline yield syntax offers the possibility to leverage complex expressions, keeping each expression its own dedicated line:

```envision
table Colors = with
  [|
    /// This is the documentation of *French*. 
    "Rouge" as French
    /// This is the documentation of *English*.
    "Red" as English 
  |]
  [| "Bleu", "Blue"  |] // A monoline yield.
  [| 
    "Vert"              // A multiline yield
    "Green" 
  |]

show table "Colors" with Colors.French, Colors.English
```

In the above script, multiline yields are introduced through line breaks in between the delimiters `[|` and `|]`. Inline markdown documentations for the fields of the table are also introduced.

## Dimensions

Dimensions can be extracted from a table comprehension or added into it. Dimensions are handy to build tables that have natural relationships predefined between them. For example, let’s consider a `Products` table that is extended into a `Variants` table by adding multiple sizes to each product. The following script illustrates this process:

```envision
table Products[Pid] = with
  [| as Product |]
  [| "shirt"    |]
  [| "pants"    |]
  [| "socks"    |]

table Variants = with
  [| as Pid, as Product, as Size |]
  [| Pid, Products.Product, "small" |]
  [| Pid, Products.Product, "medium" |]
  [| Pid, Products.Product, "large" |]

Products.Color = "black"
Variants.Color = Products.Color

show table "Variants" with
  Products.Product
  Variants.Size
  Variants.Color
```

Which displays the following table:

| Product | Size   | Color |
|---------|--------|-------|
| shirt   | small  | black |
| pants   | small  | black |
| socks   | small  | black |
| shirt   | medium | black |
| pants   | medium | black |
| socks   | medium | black |
| shirt   | large  | black |
| pants   | large  | black |
| socks   | large  | black |

The table `Products` is created via a table comprehension and it gets an autogenerated dimension named `Pid`. This opaque identifier (typed as an ordinal) does not ensure that every line in the `Product` table is distinct, it merely identifies the lines; whatever they are, in the `Products` table. Displaying the `Pid` variable is not allowed as this identifier is intended to be opaque.

Then, the table `Variants` is also created via a table comprehension. However, this time the comprehension embeds the dimension `Pid`. As the table `Variants` contains a column typed against a dimension of `Products`, this table is considered by Envision as an _extension_of the table `Products`. Thanks to this relationship, it’s possible to broadcast from `Products` to `Variants` as done in the line `Variants.Color = Products.Color`.

The above script can be simplified. The table comprehension can reuse a specific vector to be a dimension of the table (instead of using an autogenerated dimension as done above). This is done by having the name of the dimension matching the name of one of the vectors within the table comprehension. This mechanism is illustrated by:

```envision
table Products[Product] = with
  [| as Product |]
  [| "shirt"    |]
  [| "pants"    |]
  [| "socks"    |]

table Variants = with
  [| as Product, as Size |]
  [| Products.Product, "small" |]
  [| Products.Product, "medium" |]
  [| Products.Product, "large" |]

Products.Color = "black"
Variants.Color = Products.Color

show table "Variants" with
  Products.Product
  Variants.Size
  Variants.Color
```

The declared dimension `Product` for the table `Products` matches its `Product` vector. As a result, `Product` ends-up being the _text_ dimension of the `Product` table. Unlike the `Pid` variable, which was an _ordinal_, it is possible to display the dimension `Products.Product` in the table at the end of the script.

Then, the `Variants` table is simplified as it does not need two distinct vectors `Pid` and `Product`. The vector `Product` serves both to define the relationship between `Variants` and `Products` and to make the product label accessible for display.

When a vector is reused as the table dimension within a comprehension, Envision enforces _at runtime_ that each dimension value is unique. This implies that a table comprehension that features duplicate values for its dimension results in an Envision run error.
