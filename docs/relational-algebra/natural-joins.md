+++
title = "Natural joins"
description = "Parallel operations performed over all the lines of a given table are very useful, however more often than not, multiple tables are involved. Envision provides several mechanisms in order to perform operations that involve multiple tables, the most simple ones being dimensions and broadcasts, which offer the possibility to rely on natural joins."
weight = 2
+++

Parallel operations performed over all the lines of a given table are very useful, however more often than not, multiple tables are involved. Envision provides several mechanisms in order to perform operations that involve multiple tables, the most simple ones being _dimensions_ and _broadcasting_, which offer the possibility to rely on _natural joins_.

**Table of contents**
{{< toc >}}{{< /toc >}}

_Advanced remark_: the whole point of natural joins in Envision is to omit entirely the JOIN expression as found in SQL. Indeed, when writing numerical recipes, there are usually only a few joins involved, but those joins end-up being repeated _ad nauseam_ at every single step of the calculation. Envision provides mechanisms to specify the relationships between tables and then lets all the calculations flow accordingly.

## Dimensions

A dimension is a special vector that characterizes a table. A table can have several dimensions. Every primary dimension is the primary dimension of exactly one table, but some tables do not have _one_ primary dimension. The scalar table has zero primary dimension. The cross tables, discussed later, have two primary dimensions or more.

The following script creates a `Products` table that has `pid` as its primary dimension:

```envision
table Orders = with
  [| as Pid, as Date, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products[pid] = by Orders.Pid

show table "Products" with pid
```

In the script above, the table `Products` is constructed as a _grouping_ table. The dimension `pid` is the primary dimension of the table `Products` but also, by construction, a (non-primary) dimension of the table `Orders`. We will be revisiting in greater detail this table construction mechanism in the following.

Leveraging the short-name of the dimension `pid` that omits the table name, the displayed table is:

| pid    |
|--------|
| apple  |
| orange |

However, the long name of the dimension `Products.pid` could have been used instead. The logic remains identical, but the last line of the script could have been replaced by:

```envision-proto
show table "Products" with Products.pid
```

## Implicit broadcasts

For leveraging the dimensions that are found in the tables, Envision defines _broadcasting_ behaviors, which logically consists of copying the values of one table to another. During a broadcast, one line from the source table can be copied to zero or more lines to the destination tables. We say that the values of a given table can be broadcast to another table. Let’s illustrate these broadcasts with:

```envision
table Orders = with
  [| as Pid, as Date, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products[pid] = by Orders.Pid

Products.Producer = "Contoso"       // broadcast Scalar -> Products
Orders.Producer = Products.Producer // broadcast Products -> Orders

show table "Orders" with Orders.Producer
```

First, the scalar literal `"Contoso"` is broadcast to the `Products` table. This broadcast is legal because the scalar table can - by construction - be broadcast to any other table without any ambiguity. Indeed, the scalar table has a single line, thus no matter how many lines are found in the receiving table, it’s the same value that gets copied.

Second, the `Products.Producer` variable is broadcast to the `Orders` table. This broadcast is legal because `Products` is a grouping table that has been produced from `Orders` in the first place. Thus, every line in `Orders` is associated to one and exactly one line in `Products` without any ambiguity.

The most common type of broadcasts in Envision are the _implicit broadcasts_ where the expression found on the _right side_ of the assignment operator is mapped to the table specified on the table specified on the _left side_.

However, not all broadcasts are legal. For example, the following script does not compile :

```envision
table Orders = with
  [| as Pid, as Date, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products[pid] = by Orders.Pid

Orders.Producer = "Contoso"
Products.Producer = Orders.Producer // WRONG! Cannot broadcast Orders data to Products data.

show table "Products" with Products.Producer
```

While `"Contoso"` can be broadcast to `Orders` (or any table actually), the variable `Orders.Producer` cannot be broadcast to `Products`. Each `Orders` line is mapped to exactly one `Products` line, but the inverse is not true.

Envision offers many ways to create or read tables while specifying the dimensions. The dimensions are particularly interesting because they allow Envision to establish whether a table can broadcast to another table.

_Advanced remark_: While there is nothing fundamentally novel about numeric broadcasts  - Fortran has been supporting it for decades - with the advent of deep learning, there has been a renewed interest in this style of numeric operations, not only because it’s concise and elegant but also because it lends itself to a high degree of data parallelism, which nicely fits the capabilities of modern computing hardware, at least under favorable conditions. Indeed, arbitrary broadcasts - implemented as `Gather` - have a notoriously low performance on GPUs. Most deep learning toolkits feature broadcast behaviors geared around tensors, which are more suitable for high-performance computing. Envision makes these behaviors first class citizens of the language instead of delegating them to a specialized library.

**Roadmap** : The table comprehension syntax is planned to be extended to support specifying the primary dimension within the comprehension itself, instead of having it segregated into a second grouping statement as done above.

## Explicit broadcasts

While implicit broadcasts are more concise, and usually more readable as well, Envision also supports a mechanism for performing _explicit broadcasts_ at the expression level with the keyword `into`. This capability usually helps to reduce the verbosity of the Envision code, allowing to express in a single assignment what would have otherwise taken multiple lines of script.

The usage of the keyword `into` is illustrated in the following script:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

where true into Orders // explicit broadcast
  show table "Nothing filtered" with
    Orders.Pid
    Orders.OrderDate
    Orders.Quantity
```

A filter `where true` is not legal (the `Scalar` table cannot be filtered here), and furthermore, it does not point out the intended table `Orders`. The `into` keyword can be suffixed after an expression to indicate the intended table.

The script above can be rewritten in a more verbose form without using the `into` keyword with:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

Orders.IsTrue = true // implicit broadcast

where Orders.IsTrue
  show table "Nothing filtered" with
    Orders.Pid
    Orders.OrderDate
    Orders.Quantity
```

Also, it would have been possible to rewrite the script further by leveraging the table prefix syntax on literals, as illustrated by:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

where Orders.true // explicit broadcast
  show table "Nothing filtered" with
    Orders.Pid
    Orders.OrderDate
    Orders.Quantity
```

Then, a slightly more realistic example could be considered with the following script:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products[pid] = by Orders.Pid

Products.Sold = sum(Orders.Quantity)

where (Products.Sold > 4) into Orders
  show table "Only 1 order filtered" with
    pid // auto-broadcast to upstream table 'Orders'
    Orders.OrderDate
    Orders.Quantity
  
  show table "Nothing filtered" with
    pid
    Products.Sold
```

Which displays the following tables:

| Pid    | OrderDate    | Quantity |
|--------|--------------|----------|
| apple  | Apr 15, 2020 | 7        |
| apple  | Apr 16, 2020 | 3        |

and

| Pid    | Sold |
|--------|------|
| apple  | 10   |
| orange | 2    |

While it’s the `Products` table that appears in the Boolean expression of the `where` block, this expression is explicitly broadcast to the `Orders` table. As a result, the `Orders` table gets filtered, but the `Products` table does not.

## Common tables

Most operations in Envision are _vectorized_, applied element-wise over the single line of the vector(s) involved. The process is relatively simple when all the vectors belong to the same table, however, Envision also supports many situations where vectors belong to _distinct_ tables by automatically leveraging the broadcast behaviors detailed previously. In particular, the process usually boils down to identifying a **common table**. The script below illustrates this mechanism:

```envision
table Variants = with
  [| as Product, as Size |]
  [| "shirt", "small" |]
  [| "shirt", "medium" |]
  [| "pants", "small" |]
  [| "socks", "medium" |]

table Products[Product] = by Variants.Product

show table "Variants" with
  Products.Product
  Variants.Size
```

Which displays the following table:

| Product | Size   |
|---------|--------|
| shirt   | small  |
| shirt   | medium |
| pants   | small  |
| socks   | medium |

The `show` table mixes the two tables `Products` and `Variants`, and yet Envision identifies `Variants` as the proper common table, and automatically performs a broadcast of the `Products` vector toward the `Variants` table.

More generally, a common table is acceptable if any table involved in the expression or block can be broadcast to this table. This condition must be fulfilled by the common table, but this condition alone is not sufficient to identify the common table, as multiple tables may be eligible. Thus, Envision probes candidate tables in the following order:

1. Each table of the input vectors (or of the expression), starting with the first, and processing them in the script order.
2. For each vector originating from a group table, the table from which the group table was created.
3. The cross table constructed from all the dimensions found among the tables of the input vectors.

While it rarely makes sense from a supply chain perspective, it is possible to setup a situation where the common table is ambiguous, as illustrated by the following script:

```envision
table Variants[Vid] = with
  [| as Product, as Size |]
  [| "shirt", "small" |]
  [| "shirt", "medium" |]
  [| "pants", "small" |]
  [| "socks", "medium" |]

table Alts[Alt] = by [Vid, Variants.Size]
Alts.TVid, _ = Alt          // decomposing the tuple
expect Alts.Vid = Alts.TVid // add secondary dimension to 'Alts'

Alts.Foo = Variants.1 // broadcast 'Variants -> Alts'
Variants.Foo = Alts.1 // broadcast 'Alts -> Variants'

x = sum(Alts.Foo + Variants.Foo) // 'Alts' is the common table
y = sum(Variants.Foo + Alts.Foo) // 'Variants' is the common table

show summary "Resolved ambiguity" a1b1 with x, y
```

The script above creates two tables named `Variants` and `Alts`. The table `Alts`  is a group table, which will be covered in greater detail in the section _Non scalar aggregation_. The design allows the table `Alts` to be broadcast to `Variants`  as `Alts` is a group table originating from `Variants`. The design also allows the table `Variants` to be broadcast into the table `Alts` because `Alts` features `Vid` among its dimensions, which is the primary dimension of `Variants`.

Then, in the script above the operation `Alts.Foo + Variants.Foo` is ambiguous because both `Alts` and `Variants` could serve a common table. Yet, due to the rule listed above, `Alts` is probed first, hence, it is selected as the common table.

## Lookups

Lookups allow dictionary-style data accesses in Envision. A key is specified to identify a line of interest in a table. The key is intended to match a value found in the primary dimension of the table associated with the vector. The following script illustrates the lookup syntax:

```envision
table Orders[Pid] = with
  [| as Pid, as Date, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "pear",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 17), 2 |]

show scalar "" with Orders.Date["orange"] // 'Apr 17, 2020'
```

In the above script, `Orders.Date["orange"]` is the lookup operation. The key belongs to the scalar table, and as a result, the lookup result is a scalar as well.

While lookups are frequently used in many languages, from the Envision perspective, they are a bit fringe. As a rule of thumb, in Envision, natural joins should be favored whenever possible.

When performing a lookup operation, the resulting vector belongs to the same table as the one holding the key values. The following script illustrates this principle:

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

show table "Selection" a1b4 with
  Selection.Choice
  Products.Price[Selection.Choice] as "Price"
```

In the above script, `Products.Price[Selection.Choice]` evaluates as a vector that belongs to the `Selection` table.

In summary, there are two rules for lookups. First, the output table is always the same as the table in which the keys are provided. Second, all keys must be provided by that table either explicitly or implicitly. Natural joins represent the implicit flavor of the lookup: the primary dimension found in the table is used as keys. In a later section, we will see how cross tables introduce a variant of this mechanism.

It is also possible to have a lookup performed on a table upon itself as illustrated below:

```envision
table Products[product] = with
  [| as Product,   as Price, as Substitute  |]
  [| "apple",      1.50,    "pear"          |]
  [| "pear",       1.30,    "apple"         |]
  [| "orange",     2.10,    "clementine"    |]
  [| "clementine", 2.70,    "orange"        |]

show table "Products" a1d4 with
  product
  Products.Price
  Products.Substitute
  Products.Price[Products.Substitute] as "Substitute Price"
```

_Advanced remark_: Lookups in Envision are reminiscent, to some extent, to Microsoft Excel’s `VLOOKUP`. Syntax-wise, they are somewhat similar to dictionary lookups in Python, JavaScript and many other languages.

### Default and lookups

If a lookup is requested specifying a key value that is absent from the primary dimension, then the default value for the data type is used, as illustrated below:

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

show table "Selection" a1b4 with
  Selection.Choice
  Products.Price[Selection.Choice] as "Price" // '0' on 'banana'
```

However, it is also possible to specify an alternative default value through the keyword `default`, as illustrated below:

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

show table "Selection" a1b4 with
  Selection.Choice
  Products.Price[Selection.Choice] default -1 as "Price" //  '-1' on 'banana'
```

Finally, if defaulting isn't supposed to happen in the first place then `default fail` can be used to generate a runtime error, as illustrated by:

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

show table "Selection" a1b4 with
  Selection.Choice
  Products.Price[Selection.Choice] default fail
```

As a rule of thumb, if the value returned by the lookup is consumed by a later calculation - as opposed to be just immediately displayed - and if there is no "obvious" value to default to, it's advised to use `default fail`. Indeed, GIGO (garbage in, garbage out) problems are worse than clean failures while both require bugfixes anyway.

### Tuples and lookups

Tuples can also be used to perform lookups whenever a table’s primary dimension happens to be typed as a tuple. The following script illustrates this behavior with a table of _SKUs_ where the primary dimension is a tuple that includes both a _location_ and a  product _reference_:

```envision
table Raw = with
  [| as Loc, as Ref, as OnHand |]
  [| "Paris", "hat", 1 |]
  [| "Paris", "shirt", 3 |]
  [| "New York", "shirt", 2 |]
  [| "New York", "pant", 5 |]

table SKUs = by (Raw.Loc, Raw.Ref)
SKUs.OnHand = same(Raw.OnHand)

table Query = with
  [| as Loc, as Ref |]
  [| "Paris", "shirt" |]
  [| "Paris", "pant" |]
  [| "New York", "shirt"|]

show table "Query result" a1c4 with
  Query.Loc
  Query.Ref
  SKUs.OnHand[Query.Loc, Query.Ref] // 3, 0, 5
```

In the above script, the table `SKUs` is defined with a tuple as its primary dimension as the `by` keyword gets two vectors as arguments. The last line `SKUs.OnHand[Query.Loc, Query.Ref]` is the tuple lookup itself, which returns 0 (zero) if the entry is not found in the primary dimension of `SKUs`.

<!-- https://lokad.atlassian.net/browse/LK-8286 The example should be simplified with a direct tuple declaration for its primary dimension. -->
