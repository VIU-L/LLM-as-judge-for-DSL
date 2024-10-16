+++
title = "Aggregating"
description = "Aggregation, i.e. combining multiple values into one, is ubiquitous in Envision and many other programming languages. The most widely used aggregators, that is functions that perform aggregation, are probably 'sum' and 'average', however there are many others. In Envision, aggregators are a special case of processes, a class of functions that benefit from special capabilities that make them more versatile. In this section, we focus on the aggregation angle, but we will get back to their processes in the later section 'User Defined Functions'."
weight = 4
+++

Aggregation, i.e. combining multiple values into one, is ubiquitous in Envision and many other programming languages. The most widely used aggregators, that is functions that perform aggregation, are probably _sum_ and _average_, however there are many others. In Envision, aggregators are a special case of _processes_, a class of functions that benefit from special capabilities that make them more versatile. In this section, we focus on the aggregation angle, but we will get back to their processes in the later section _User Defined Functions_.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Syntax overview

Let’s introduce some terminology. The extended form of an aggregation expression - putting aside `cross` aggregations and their `scan` variants for now - simply referred to as an _aggregation_ in the following, is:

```envision-proto
agg(S.A1, S.A2; G.B1, G.B2)  when S.C1 sort [S.D1, S.D2] default O.E1  by [S.F1, S.F2] at [O.G1, O.G2]
```

where:

* `agg()` is an aggregator, such as `sum()`.
* `S` is the source table
* `G` is the group table
* `O` is the output table
* `S.A1`, `S.A2` are the regular arguments (comma-separated)
* `;` is the delimiter indicating the start of the group arguments
* `G.B1`, `G.B2` are the group arguments (comma-separated)
* `when`, `sort`, `default`, `by` and `at` are options

The **source table** is defined by the regular arguments. The `sort` option, when present, always defines a tuple in this table. The `by` option usually defines a tuple in this table, otherwise it defines a tuple in a table that can be broadcast to the source table.

The **group table** can be broadcast to the source table. It is defined by the group arguments, when present, that is arguments that follow the semicolon `;`. Otherwise, it is defined by the group table formed with the `by` option. When there is no `by` option specified either then the default `into` table is used instead.

The **output table** is the table that contains the results. The group table can be broadcast to the output table. This table is frequently equal to the group table, making the broadcast trivial. However, when no broadcast is available by default, the `at` option can be used to ensure matching between the `by-at` pairs of tuples.

Aggregations can appear in several contexts. The most common context is the assignment `R.Foo = sum(S.Bar)`, however aggregations can also appear in filters `where sum(S.Bar) > 0` or among the tile inputs.

All these concepts are probably still fuzzy to the reader at this point. In this section, we will be covering the fine print of all the aggregation mechanisms.

## Scalar aggregation

Aggregators, as the name suggests, combine multiple values into one. Envision supports a whole library of aggregators. Let’s start with the _sum_:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

show summary "My Sum" with sum(Orders.Quantity)
```

The script above displays the sum of all the values found in the vector `Orders.Quantity`. More specifically, it performs an aggregation from the `Orders` table to the `Scalar` table. This script could be rewritten in a slightly more verbose and more explicit manner:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

Scalar.mySum = sum(Orders.Quantity)

show summary "My Sum" with Scalar.mySum
```

The aggregation works between the table `Orders` and the table `Scalar` because it’s possible to implicitly broadcast from `Scalar` to `Orders` (by design, it’s possible to broadcast from `Scalar` to any table). More generally, if it’s possible to broadcast from table A to table B, then it’s possible to aggregate from table B to table A.

However, it’s not possible to perform arbitrary aggregation from any table to any table - at least not without resorting to options that will be detailed later. For example:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

Scalar.Foo = 42
Orders.NotWorking = sum(Scalar.Foo) // WRONG! Cannot aggregate from Scalar to Orders.
```

The script above does not compile because Envision cannot aggregate from `Scalar` to `Orders`. In the present situation, the illegal aggregation is nonsensical. However, as we will see in the following, there are situations where the aggregation could make sense and yet where tables lack broadcast relationships.

As hinted above, there is a whole catalog of aggregators in Envision. The script below illustrates some of the most widely used:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

show summary "More aggregators" with
  sum(Orders.Quantity)
  avg(Orders.Quantity)
  max(Orders.Quantity)
  median(Orders.Quantity)
  mode(Orders.Pid)
```

Aggregators exist for (almost) all data types. They are not restricted to numeric data types as illustrated with `mode(Orders.Pid)`, which returns the most frequent text value of the column `Orders.Pid`.

Scalar aggregation is frequently used, and Envision offers a syntactic sugar `by 1` to express this aggregation in a rather concise manner as illustrated by:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

Orders.Total = sum(Orders.Quantity) by 1
total = same(Orders.Total)
show label "\{total}"
```

The expression `sum(Orders.Quantity) by 1` is strictly equivalent to its slightly more verbose counterpart `sum(Orders.Quantity) into Scalar`. Intuitively, using a constant for the grouping key implies that there is only a single group, hence a scalar aggregation. However, the `by 1` is a special case in the Envision syntax, and attempting to write `by 42` or any other constant does not work.

## Non-scalar aggregation

There are situations where the goal is to compute an aggregate for every line of a given table, instead of aggregating everything down to a single (scalar) value. For example, we might want to compute the total number of units sold per per product for every product:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products[pid] = by Orders.Pid

Products.Sold = sum(Orders.Quantity)

show table "Products" with
  pid
  Products.Sold
```

Which displays the following table:

| pid    | Sold |
|--------|------|
| apple  | 10   |
| orange | 2    |

The aggregation `sum(Orders.Quantity)` works because there is a broadcast relationship from `Products` to `Orders` in place from the way the table `Products` has been constructed, i.e. as a group table over the table `Orders`.

The script above is strictly equivalent to:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products[pid] = by Orders.Pid

show table "Products" with
  pid
  sum(Orders.Quantity) into Products as "Sold"
```

Where the `into` keyword is used to specify the aggregation target table of `sum(Orders.Quantity)`.

However, if the `Products` table has been obtained without specifying its relationship with `Orders`, there would not be any broadcast relationship between the two tables, and thus, the natural aggregation would not work. In this case, it is possible to specify the keys to be used as illustrated by:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products = with
  [| as Pid |]
  [| "apple" |]
  [| "orange" |]

Products.Sold = sum(Orders.Quantity) by Orders.Pid at Products.Pid

show table "Products" with
  Products.Pid
  Products.Sold
```

The two keywords `by` and `at` are **aggregator options** used to specify the source vector(s) and the destination vector(s) respectively used for the grouping operation. Here, those options are the exact _explicit_ equivalent of their _implicit_ counterpart (omitting the by-at) illustrated by the first script of the present section.

For the sake of clarity, Envision does not allow expliciting the by-at options when the chosen options duplicate the implicit one. Indeed, the primary purpose of the natural joins provided by Envision is to provide a more concise alternative to SQL joins.

<!-- TODO: example using only the ‘by’, not the ‘at’ -->

## Multi-dimensional aggregation

Envision allows aggregation over multiple dimensions. The syntax leverages brackets `[` and `]` as delimiters, used to list the inner vectors of the dimension. From the Envision perspective, a dimension can be _complex_ and involve multiple vectors. Let’s examine the following script:

```envision
table Shipments = with
  [| as Product, as Origin, as OrderDate, as Quantity |]
  [| "apple", "France", date(2020, 4, 15), 3 |]
  [| "apple", "Spain", date(2020, 4, 16), 7 |]
  [| "orange", "Italy", date(2020, 4, 16), 2 |]
  [| "apple", "France", date(2020, 4, 17), 5 |]

table Routes[pair] = by [Shipments.Product, Shipments.Origin]

Routes.Product, Routes.Origin = pair

Routes.Incoming = sum(Shipments.Quantity)

show table "Routes" with
  Routes.Product
  Routes.Origin
  Routes.Incoming
```

Which displays the following table:

| Product | Origin | Incoming |
|---------|--------|----------|
| apple   | France | 8        |
| apple   | Spain  | 7        |
| orange  | Italy  | 2        |

The group table `Routes` is constructed by aggregating over two dimensions `Shipments.Products` and `Shipments.Origin`: one grouping is created for any observed distinct pair of values. As a consequence, the primary key `pair` of the table `Routes` is a _pair_ of dimensions. This complex dimension is deconstructed, just like a tuple, as `Routes.Product` and `Routes.Origin`. Those `Routes` vector names are chosen for consistency with their original `Shipments` counterparts, however, it would have been possible to name those two vectors differently.

The aggregation `sum(Shipments.Quantity)` leverages that the `Routes` table can be broadcast to the `Shipments` table, just like we did in the previous section with `Products` and `Orders` respectively.

## Explicit output table

Gaining control over the output table offers the possibility to join two arbitrary tables via an aggregation. This mechanism is achieved with the `by-at` options, which are used as a pair for this purpose. Let’s revisit a variant of the example used in the previous section with:

```envision
table Shipments = with
  [| as Product, as Origin, as OrderDate, as Quantity |]
  [| "apple", "France", date(2020, 4, 15), 3 |]
  [| "apple", "Spain", date(2020, 4, 16), 7 |]
  [| "orange", "Italy", date(2020, 4, 16), 2 |]
  [| "apple", "France", date(2020, 4, 17), 5 |]

table Routes = with
  [| as Product, as Origin |]
  [| "apple", "France" |]
  [| "apple", "Spain" |]
  [| "orange", "Italy" |]

Routes.Incoming = sum(Shipments.Quantity)
  by [Shipments.Product, Shipments.Origin]
  at [Routes.Product, Routes.Origin]

show table "Routes" with
  Routes.Product
  Routes.Origin
  Routes.Incoming
```

As the by-at expression used to define `Routes.Incoming` is somewhat verbose, the statement is split over 3 lines, leveraging the line continuation rules of Envision. The brackets `[` and `]` are used for the by-at options, with a syntax aligned with the declaration of a group table in the first script of this section.

The `at` option is used to define a group table over the output table (referred to as the left group table) and then bind it with the group table produced on top of the source table (referred to as the right group table). The final results are obtained by a broadcast from the right group table to the left group table. Left groups that don’t have any counterpart on the right side are replaced by default values on empty groups, this mechanism is revisited in the subsection “Empty Groups” below.

There are no particular limits to the number of dimensions that can be used as part of an aggregation, however beyond four, it’s probably a good idea to start investigating how the script can be refactored to avoid having so many dimensions involved.

_Advanced remarks_:  Most of the `JOIN` operations done in SQL can be removed with the `by-at` options offered by Envision. With most SQL databases, performing joins without proper indexes in place results in an atrocious performance. This is not the case in Envision. The necessary indexes are constructed on the fly during the execution, and the amount of compute resources tend to be proportional to the compressed size of the vectors involved.

## Group table rules

**In assignments**, the group table of an aggregation is frequently specified with the option `by` and sometimes specified through the option `default`. However, when both options are omitted, then the **left table rule** applies: an implicit `into T` option is added to the function call where `T` is the table found on the left side of the assignment and this table `T` is used as the group table. This rule is illustrated by:

```envision
table Products = with
  [| as Product, as Color, as Price |]
  [| "pants", "blue", 25 |]
  [| "shirt", "pink", 15 |]
  [| "shirt", "white", 15 |]
  [| "socks", "green", 5|]

Scalar.AvgPrice = avg(Products.Price) // 'into Scalar'

show scalar "My average price" with Scalar.AvgPrice
```

In the above script, the aggregator `avg()` (which computes the average) has no option `by` specified. Thus, the left table rule applies, and as the table found on the left is `Scalar`, the expression is implicitly rewritten as `avg(Products.Price) into Scalar`.

The left table rule only applies to aggregators, it does not apply to other non-aggregator functions that support a `by` option, such as `percent()` or `rank()`. However, it applies to all aggregator calls no matter their nesting status. For example, considering three tables `T`, `U` and `V` then `T.C = sum(sum(U.A) + V.B)` is rewritten to `T.C = sum(sum(U.A) into T + V.B) into T`, which is rarely the intended semantic.

The left table rule defines the default `into` table for aggregations. However, once `into` is explicitly specified, this newer table propagates to all the inner expressions.  For example, considering three tables `T`,  `U` and `V`, then `(sum(T.A) + sum(U.B)) into V` is rewritten as `(sum(T.A) into V) + (sum(U.B) into V)`.

**In tiles**, the default group table depends on the tile itself. The tiles `scalar`, `summary` and `form` use `Scalar` table as their default. The `linechart` tile uses the `Day` table as its default - this aspect will be revisited in the later section “Calendar Elements”. Also, when the options `group by` and `group into` are provided at tile level, those options also override the default group table. These tile options are covered in the later subsection “In-tile aggregation”.

**In filters**, when the `where` filter (resp. the `when` filter) is used, the default group table is the `Items` table (resp. the `Day` table). Both the `Items` and the `Day` tables are special cases in Envision. These two tables will be discussed later in the “Reading files” section.

## Empty groups

Aggregators face an edge case on empty groups. While certain situations lend themselves to intuitive defaults, like assuming that the _sum_ of an empty set of numbers is zero (it is the case with Envision), it’s unclear what the _mode_ (most frequent values) should be. Every data type in Envision has its own _default value_ which is used as a fall-back for an aggregation when there is no value to aggregate.

The most common default values are:

* `0` (zero) for numbers
* `""` (empty text) for texts
* `false` for Booleans
* `2001-01-01` for dates
* Dirac on zero for ranvars
* 0 (zero function) for zedfuncs

However, aggregators also offer an option `default` that allows to specify which value should be used when the group is empty. For example:

```envision
table Few = with
  [| as Something |]
  [| "foo" |]
  [| "bar" |]

table EmptySet = where Few.Something == "qux"

myResult = max(EmptySet.Something) default "nothing!"

show summary "Agg on Empty" with myResult
```

The script above displays `nothing!` which is the fallback associated with the aggregation `max(EmptySet.Something)`.

Then, Envision supports regular _vector_ values to be used for aggregation fallback, not merely scalar values.

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products = with
  [| as Pid, as MyDefault |]
  [| "apple",  -1 |]
  [| "orange", -2 |]
  [| "banana", -3 |]

Products.Sold = sum(Orders.Quantity)
  default Products.MyDefault
  by Orders.Pid
  at Products.Pid

show table "Products" with
  Products.Pid
  Products.Sold
```

Which displays:

| Pid    | Sold |
|--------|------|
| apple  | 10   |
| orange | 2    |
| banana | -2   |

The script above leverages `default Products` to define the fallback when an empty group is encountered within `sum(Orders.Quantity)`. Also, the aggregation is using three options `default`, `by` and `at`, leveraging the line continuation (detailed previously) of Envision to make the code more readable. It would have been possible, but less readable, to keep the 4 lines used to define `Products.Sold` into a single one omitting the line breaks.

The `default` option is a **group option**: it is expected to be aligned with the group rather than being aligned with the argument(s). From a syntax perspective, when aggregating from a source table `S` to a group table `T` we have `T.Foo = sum(S.Bar) by S.Foo default T.Qux`. More generally, the `default` option can be used with any table and can be broadcast to the group table.

## Group arguments

Some aggregators, as well as some other functions, can take arguments that are aligned with the group table, rather than being aligned with the source table. The `join()` aggregator that concatenates text values is one of them. It takes a regular argument for the text values to be concatenated and a **group argument** for the delimiter (also a text value) to be used for each group. The syntax is illustrated by:

```envision
table Variants = with
  [| as Product, as Color, as Limit  |]
  [| "pants", "blue", " " |]
  [| "shirt", "pink", ", " |]
  [| "shirt", "white", ", " |]
  [| "socks", "green", " - " |]
  [| "socks", "yellow", " - " |]

table Products[product] = by Variants.Product
Products.Limit = same(Variants.Limit)

Products.Colors = join(Variants.Color; Products.Limit)
                  sort Variants.Color

show table "Colors" with
  product
  Products.Colors
```

Which displays the following table:

| product | Colors         |
|---------|----------------|
| pants   | blue           |
| shirt   | pink, white    |
| socks   | green - yellow |

The above script leverages the `join()` aggregator to define `Products.Color`. The function takes a first (regular) argument `Variants.Color` but also a second group argument `Products.Limit`. Beware, the delimiter `;` is used to introduce the group arguments. Thus, the character `;` is used - instead of the usual comma `,` - to delimit the two arguments of `join()`. Prior to this, the aggregator `same()` is used to define `Products.Limit`. This aggregator returns the value that is expected to be identical across all the grouped lines.

The general function call syntax is `myFun(a1, a2, a3; g1, g2, g3)` where both regular arguments `aX` and group arguments `bX` are comma-delimited, and where the semi-colon `;` is used to separate the two lists. This syntax will be revised more extensively when discussing the user defined functions in the following.

## Filtered aggregation

Aggregators also support the option `when`, which provides an inline filtering mechanism similar to the one provided by the `where` blocks. The following script illustrates the `when` filter’s syntax:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products = with
  [| as Pid, as MyDefault |]
  [| "apple",  -1 |]
  [| "orange", -2 |]
  [| "banana", -3 |]

Products.Sold = sum(Orders.Quantity)
  when (Orders.OrderDate < date(2020, 4, 16))
  default Products.MyDefault
  by Orders.Pid
  at Products.Pid

show table "Products" with
  Products.Pid
  Products.Sold
```

Which displays the default values for the two products that didn’t have any orders to aggregate:

| Pid    | Sold |
|--------|------|
| apple  | 10   |
| orange | -3   |
| banana | -2   |

The expression `when (Orders.OrderDate < date(2020, 4, 16))` is put between parentheses `(` and `)` due to conflicting operator priorities between `<` and `default`.

This script happens to be strictly equivalent to the variant below that leverages a `where` block:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products = with
  [| as Pid, as MyDefault |]
  [| "apple",  -1 |]
  [| "orange", -2 |]
  [| "banana", -3 |]

where (Orders.OrderDate < date(2020, 4, 16))
  Products.Sold = sum(Orders.Quantity)
    default Products.MyDefault
    by Orders.Pid
    at Products.Pid

  show table "Products" with
    Products.Pid
    Products.Sold
```

However, the `when` option cannot always be trivially replaced by a `where` block. For example, the following script:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products[pid] = by Orders.Pid

Products.Sold = sum(Orders.Quantity) when (pid != "apple")

show table "Products" with
  pid
  Products.Sold
```

Displays the following table:

| Pid    | Sold |
|--------|------|
| apple  | 0    |
| orange | 2    |

While its `where` counterparts:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products[pid] = by Orders.Pid

where pid != "apple"
  Products.Sold = sum(Orders.Quantity)

  show table "Products" with
    pid
    Products.Sold
```

Only display:

| Pid    | Sold |
|--------|------|
| orange | 2    |

Omitting the `apple` line entirely. This behavior is caused by the `where` block, which captures the final `show` statement in the script above. However, it’s not possible to just end the `where` block _before_ the `show` statement, because then the script does not compile any more as illustrated by:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products[pid] = by Orders.Pid

where pid != "apple"
  Products.Sold = sum(Orders.Quantity)

show table "Products" with
  Products.Pid
  Products.Sold // WRONG! Undefined variable 'Products.Sold'.
```

The final line `Product.Sold` is invalid because, as pointed out in the previous _Filtering_ section, the vector `Product.Sold` is only defined in a filtered scope, and Envision prevents the use of a potentially undefined vector in the non-filtered outer scope.

## Ordered aggregation

While most aggregators do not depend on the ordering of the elements in the grouping, ordering does matter for certain aggregators, most notably `first()` and `last()`. With those order-sensitive aggregators, the `sort` option must be used to specify the proper order, as illustrated by:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products[pid] = by Orders.Pid

Products.LastQuantity = last(Orders.Quantity) sort Orders.OrderDate

show table "Products" with
  pid
  Products.LastQuantity
```

Which displays the following table:

| pid    | LastQuantity |
|--------|--------------|
| apple  | 7            |
| orange | 2            |

Attempting to use the `sort` option with an aggregator that does not depend on ordering the grouped values, like `max()`, results in a compile-time error.

## Cartesian products

In mathematics, the Cartesian product of two sets _A_ and _B_, denoted _A × B_, is the set of all ordered pairs _(a, b)_ where _a_ is in _A_ and _b_ is in _B_. Envision offers capabilities to generate and process Cartesian products. Let’s consider a situation with a list of stores and a list of products. Each store has an affinity to two segments of customers referred to as _population A_ and _population B_. Also, each product has an affinity to each customer segment. Let’s see how to the total affinity crossing all products against all stores can be computed in Envision using the `cross` aggregation option:

```envision
table Pr = with // Products
  [| as Pid, as PopA, as PopB |]
  [| "apple", 0.5, 0.5 |]
  [| "banana", 0.2, 0.8 |]
  [| "orange", 0.6, 0.4 |]

table St = with // Stores
  [| as City, as PopA, as PopB |]
  [| "Paris", 0.9, 0.1 |]
  [| "Lyon", 0.7, 0.3 |]
  [| "Tours", 0.5, 0.5 |]
  [| "Lille", 0.6, 0.4 |]

Pr.Affinity = sum(Pr.PopA * St.PopA + Pr.PopB * St.PopB) cross(Pr, St)

affinity = sum(Pr.Affinity)

show label "\{affinity}"
```

In the script above, the total affinity is computed in two steps. First, we compute `Pr.Affinity` by doing a cross-aggregation over the tables `Pr` and `St`. This calculation involves a simple multiplication of _product affinity_ times _store affinity_, done both for the populations A and B. Second, the total `affinity` is computed as a regular aggregation from the `Pr` table in the `Scalar` table.

The `cross` option indicates that the aggregation must be done targeting the first (i.e. left) table passed as an argument. Unless other aggregation options are used, as detailed below, the compute cost for this operation is quadratic: the number of lines of the first table multiplied by the number of lines of the second table. While Cartesian products can be handy, bear in mind that if the tables are large, this operation can become expensive computer-wise.

_Advanced remark_ : Under the hood, Lokad makes serious attempts to ensure that the cross table is not _reified_, that is, that the whole computation is done online, with an amount of memory that does not exceed the sum of memory required to process the tables involved in the crossing. This approach does not mitigate the superlinear _compute cost_ of the Cartesian product, but it does largely mitigate its _memory cost_. Also, while the compute time grows super linearly, the wall-clock time of the execution is not linearly correlated to the compute time (up to a point) as Lokad extensively distributes the workload over many CPUs. Nevertheless, the increase in _cost_ is linear to the complexity of the Cartesian product.

It is also possible to perform a Cartesian product of a table with itself. Let’s consider the case of a similarity search where one wants to find the most similar, but distinct, element of the table according to a given metric. Let’s revisit our previous example crossing the `St` (stores) table with itself:

```envision
table St = with // Stores
  [| as City, as PopA, as PopB |]
  [| "Paris", 0.9, 0.1 |]
  [| "Lyon", 0.7, 0.3 |]
  [| "Tours", 0.5, 0.5 |]
  [| "Lille", 0.6, 0.4 |]

St.Twin = first(St2.City)
  sort (abs(St.PopA - St2.PopA) + abs(St.PopB - St2.PopB))
  when (St.City != St2.City)
  cross(St, St as St2)

show table "Twins" with St.City, St.Twin
```

Which displays:

| City  | Twin  |
|-------|-------|
| Paris | Lyon  |
| Lyon  | Lille |
| Tours | Lille |
| Lille | Lyon  |

There are a series of notable elements in the script above. First, the `sort` option, which was introduced in the previous section, is used to order the result according to our _ad hoc_ similarity metric. Second, the `when` option, also introduced previously, is used to eliminate the diagonal lines of the Cartesian product (i.e. a line crossed with itself). Finally, the keyword `as` is used within the `cross` option to rename `St` as `St2`. This syntactic sugar gives Envision access to a clone table named `St2`.

Beware the `sort` option, which when used in conjunction with the `cross` option, sorts the grouped elements of the table on the _right_ of the `cross`. There is no ordering involved for the elements of the table to the _left_ of the `cross`.

It would have been possible to have the exact same behavior without resorting to an inline clone table but using a regular clone table, as introduced previously. The following script gives identical results compared to the previous one:

```envision
table St = with // Stores
  [| as City, as PopA, as PopB |]
  [| "Paris", 0.9, 0.1 |]
  [| "Lyon", 0.7, 0.3 |]
  [| "Tours", 0.5, 0.5 |]
  [| "Lille", 0.6, 0.4 |]

table St2 = where St.*

St.Twin = first(St2.City)
  sort (abs(St.PopA - St2.PopA) + abs(St.PopB - St2.PopB))
  when (St.City != St2.City)
  cross(St, St2)

show table "Twins" with St.City, St.Twin
```

However, when using the inline form, i.e. `cross(St, St as St2)`, the table `St2` is locally scoped to the aggregation expression, and cannot be used afterward. Thus, if the clone table is only needed for the `cross` aggregation then we recommend to do it inline for the sake of concision.

The previous example is an exhaustive similarity search that processes every single pair of lines within the table. Let’s refine this example with an additional assumption: the only pairs that are eligible for similarity search are those within the same region. This script variant illustrates this additional constraint:

```envision
table St = with // Stores
  [| as City, as PopA, as PopB, as Region |]
  [| "Paris", 0.9, 0.1, "North" |]
  [| "Lyon", 0.7, 0.3, "South" |]
  [| "Tours", 0.5, 0.5, "North" |]
  [| "Lille", 0.6, 0.4, "North" |]
  [| "Cannes", 0.8, 0.2, "South" |]

St.Twin = first(St2.City)
  sort (abs(St.PopA - St2.PopA) + abs(St.PopB - St2.PopB))
  when (St.City != St2.City and St.Region == St2.Region)
  cross(St, St as St2)

show table "Twins" with St.City, St.Twin
```

Which displays the following table:

| City   | Twin   |
|--------|--------|
| Paris  | Lille  |
| Lyon   | Cannes |
| Tours  | Lille  |
| Lille  | Tours  |
| Cannes | Lyon   |

The condition `St.Region == St2.Region` ensures that similarities are only probed _within_ the same region. However, compute-wise, we have not gained anything because Envision still probes every single pair. Ideally, we would like to have Envision only probing the sub-products within each distinct `St.Region`. This can be done by using `by-at` as illustrated below.

However, due to the design of `cross`, which relies on the assumption that the cross table won’t be reified, the `sort` can only be applied to the right table (here `St2`) when used in conjunction with `by-at`. However, in the script above the `sort` option leverages both the right and left tables. Thus, in order to demonstrate how the `by-at` can be used, we first need to remove the need for the `sort` option.

The following script is strictly equivalent to the previous one, but the `first() sort` combo has been replaced by the `argmin()` aggregator:

```envision
table St = with // Stores
  [| as City, as PopA, as PopB, as Region |]
  [| "Paris", 0.9, 0.1, "North" |]
  [| "Lyon", 0.7, 0.3, "South" |]
  [| "Tours", 0.5, 0.5, "North" |]
  [| "Lille", 0.6, 0.4, "North" |]
  [| "Cannes", 0.8, 0.2, "South" |]

St.Twin =
  argmin (abs(St.PopA - St2.PopA) + abs(St.PopB - St2.PopB), St2.City)
  when (St.City != St2.City and St.Region == St2.Region)
  cross(St, St as St2)

show table "Twins" with St.City, St.Twin
```

The complex aggregator `argmin()` takes two arguments. The first argument is the ordering criterion and the second argument is the value to be returned for the line of the grouping that reaches the minimal value (as per the first argument).

Now that the `sort` option has been removed, it becomes possible to replace the `when` option above by its equivalent `by-at` counterpart as illustrated by:

```envision
table St = with // Stores
  [| as City, as PopA, as PopB, as Region |]
  [| "Paris", 0.9, 0.1, "North" |]
  [| "Lyon", 0.7, 0.3, "South" |]
  [| "Tours", 0.5, 0.5, "North" |]
  [| "Lille", 0.6, 0.4, "North" |]
  [| "Cannes", 0.8, 0.2, "South" |]

St.Twin =
  argmin (abs(St.PopA - St2.PopA) + abs(St.PopB - St2.PopB), St2.City)
  when (St.City != St2.City)
  cross(St, St as St2)
  by St2.Region at St.Region

show table "Twins" with St.City, St.Twin
```

The script just above produces the same results as the previous one, however by introducing a grouping mechanism through `by-at` the compute cost can be vastly reduced. Indeed, instead of processing all the pairs of lines between the two tables, only the pairs _within_ the same groups, as identified through the `by-at` options, are investigated.

While the example above is tiny, let’s consider a situation where there are 10,000 locations. Crossing those locations with themselves would require 10,000 x 10,000 = 100 millions pairs to be processed. However, if the locations can instead be grouped in 20 groups of 500 locations, then the crossing would only require 500 x 500 x 20 = 5 million pairs to be processed.

Most operations in Envision are safe-by-design in terms of performance. However, cross tables are one of the few operations that are involved in superlinear compute costs, which may come as a surprise. Thus, whenever considering using `cross`, we suggest to first do a back-of-the-envelope calculation to make sure that the number of pairs to be processed is not unreasonably large. As a rule of thumb, if the number of pairs is below 1 billion, it’s unlikely to be a problem production-wise; beyond 1 billion pairs, tread cautiously.

## Range filters

Aggregations over ranges, typically but not exclusively time ranges, are useful. For example, computing the moving average of a time-series is an example of a range aggregation. The keyword `over` provides a powerful mechanism. Let’s illustrate how to use `over` to compute a 2-day moving average:

```envision
table Orders = with
  [| as Product, as OrderDate, as Quantity |]
  [| "banana", date(2020, 4, 14), 5 |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]
  [| "banana", date(2020, 4, 17), 2 |]

Orders.Mavg = sum(Orders.Quantity)
  by Orders.Product
  over Orders.OrderDate = [-1 .. 0]

show table "Moving average over 2 days" with
  Orders.Product
  Orders.OrderDate
  Orders.Mavg
```

Which displays the following table:

| Product | OrderDate    | Mavg |
|---------|--------------|------|
| banana  | Apr 14, 2020 | 5    |
| apple   | Apr 15, 2020 | 3    |
| apple   | Apr 16, 2020 | 10   |
| banana  | Apr 17, 2020 | 2    |
| orange  | Apr 16, 2020 | 2    |

The above script leverages the aggregation option `over Orders.OrderDate = [-1 .. 0]` in order to specify that the eligible time range is the current date, as defined by `Orders.OrderDate` minus one day up to `Orders.OrderDate` itself.

The range specified by `over` is inclusive, and relative to the vector identified on the left side of the assignment. The option `over` works with data types that support both a comparer and the addition with a number. In practice, `over` is used with numbers and dates.

Under the hood, the `over` option leverages a cross table. In order to illustrate this mechanism, the script above can be rewritten with a `cross` option instead:

```envision
table Orders = with
  [| as Product, as OrderDate, as Quantity |]
  [| "banana", date(2020, 4, 14), 5 |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]
  [| "banana", date(2020, 4, 17), 2 |]

Orders.Mavg = sum(Orders2.Quantity)
  cross(Orders, Orders as Orders2)
  by Orders2.Product at Orders.Product
  when (Orders2.OrderDate >= Orders.OrderDate + (-1) and
        Orders2.OrderDate <= Orders.OrderDate + (0))

show table "Moving average over 2 days" with
  Orders.Product
  Orders.OrderDate
  Orders.Mavg
```

As discussed in the previous section, the use of `cross` entails a superlinear compute cost, and the same consideration applies to the `over` option.

Then, the `over` range is required to be made of number literals. Any expression that can be broadcast to the table being aggregated - `Orders` in the script above - can be used. For example, the script below illustrates a more dynamic moving average with the time range - in days - that varies from one product to the next.

```envision
table Orders = with
  [| as Product, as OrderDate, as Quantity |]
  [| "banana", date(2020, 4, 14), 5 |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]
  [| "banana", date(2020, 4, 17), 2 |]

table Products[Product] = by Orders.Product

Products.Range = if Product != "banana" then 1 else 7

Orders.Mavg = sum(Orders.Quantity)
  by Orders.Product
  over Orders.OrderDate = [-Products.Range .. 0]

show table "Moving average over 2 days" with
  Orders.Product
  Orders.OrderDate
  Orders.Mavg
```

Which displays the following table:

| Product | OrderDate    | Mavg |
|---------|--------------|------|
| banana  | Apr 14, 2020 | 5    |
| apple   | Apr 15, 2020 | 3    |
| apple   | Apr 16, 2020 | 10   |
| banana  | Apr 17, 2020 | 7    |
| orange  | Apr 16, 2020 | 2    |

In the script above the line `Products.Range = if Product then "banana" else 1 : 7` uses a ternary `if` in order to define a range that equals to 1 for all products, except `banana` which gets a range equal to 7. As a result, the second `banana` line in the result table above is 7, while it was 2 in the first script introduced in this section.

The `over` also has some built-in behavior for cross tables that contains a date dimension. We will be revisiting this specific angle in the section “Calendar elements” in the following.

## Iterated aggregation

The iterated aggregation is a specialized variant of the aggregation over the Cartesian product, which is useful when performing _iterated_ computations like cumulative sums. The keyword `scan` is introduced for this purpose as illustrated by:

```envision
table Orders = with
  [| as Product, as OrderDate, as Amount |]
  [| "pants", date(2020, 5, 1), 25 |]
  [| "shirt", date(2020, 5, 2), 15 |]
  [| "shirt", date(2020, 5, 3), 15 |]
  [| "socks", date(2020, 5, 3), 5|]
  [| "pants", date(2020, 5, 4), 25 |]

Orders.SoldSoFar = sum(Orders.Amount) scan Orders.OrderDate

show table "Cumulative sales" with
  Orders.Product
  Orders.OrderDate
  Orders.Amount
  Orders.SoldSoFar
```

Which displays the following table:

| Product | OrderDate   | Amount | SoldSoFar |
|---------|-------------|--------|-----------|
| pants   | May 1, 2020 | 25     | 25        |
| shirt   | May 2, 2020 | 15     | 40        |
| shirt   | May 3, 2020 | 15     | 55        |
| socks   | May 3, 2020 | 5      | 60        |
| pants   | May 4, 2020 | 25     | 85        |

In the above script, through the `scan` option, the table `Orders` is crossed with itself, and then an aggregation of incrementally larger groups is produced following the order specified through the `scan` option itself, i.e. `Orders.OrderDate`. The smallest group starts with the first line of the `Orders` table (according to the order specified through `Orders.OrderDate`) and ends with the entire table.

When the `scan` option is used, the resulting table is the same as the source table passed as an argument to the aggregator, i.e. `Orders` above. Also, the `scan` option implicitly acts as a `sort` option, thus the `scan` option cannot be used in conjunction with the `sort` that it supersedes.

It is possible to _partition_ the process through the `by` option. In this case, the iterated aggregation is performed for each group independently as illustrated by:

```envision
table Orders = with
  [| as Product, as OrderDate, as Amount |]
  [| "pants", date(2020, 5, 1), 25 |]
  [| "shirt", date(2020, 5, 2), 15 |]
  [| "shirt", date(2020, 5, 3), 15 |]
  [| "socks", date(2020, 5, 3), 5|]
  [| "pants", date(2020, 5, 4), 25 |]

Orders.SoldSoFar = sum(Orders.Amount)
                   by Orders.Product
                   scan Orders.OrderDate

show table "Cumulative sales" with
  Orders.OrderDate
  Orders.Amount
  Orders.SoldSoFar
```

Which displays the following table:

| Product | OrderDate   | Amount | SoldSoFar |
|---------|-------------|--------|-----------|
| pants   | May 1, 2020 | 25     | 25        |
| shirt   | May 2, 2020 | 15     | 15        |
| shirt   | May 3, 2020 | 15     | 30        |
| socks   | May 3, 2020 | 5      | 5         |
| pants   | May 4, 2020 | 25     | 50        |

In the above script, the cumulative sums are still happening, but restricted to the three distinct groups as defined by `Orders.Product`.

The `scan` option is logically a cross of the source table with itself. Let’s consider a `scan` on the table `T` with a generic aggregator `agg()` :

```envision-proto
T.MyScan = agg(T.Foo) by T.Bar scan T.Qux
```

This statement is (almost) logically equivalent to the following statement:

```envision-proto
T.MyRank = rank() by T.Bar sort T.Qux
T.MyScan = agg(T2.Foo)
  sort T2.MyRank // only if 'agg' needs it
  when (T.Bar == T2.Bar and
        T.MyRank <= T2.MyRank)
  cross (T, T as T2)
```

While the above script is not exactly valid Envision code, the `rank()` function does exist in Envision and returns the rank (integers starting at 1) of the line within the group against the specified ordering. Once `T.MyRank` is defined, the cross emulates the iterated aggregation produced by the option `scan`. However, as some aggregators like `sum()` don’t depend on the ordering, the line `sort(T.MyRank)` would have to be omitted for those aggregators.

The `scan` option is supported for all aggregators except `distinct()`, `entropy()`, `median()`, `mode()`, `whichever()` and the aggregators that return either ranvars or zedfuncs. Indeed, while the `scan` is logically equivalent to a cross, it is possible to provide fast implementations with linear or quasi-linear compute costs for most aggregators. The supported aggregators fall into this category, and the implementation provided by Lokad does not incur quadratic compute costs.

## In-tile aggregation

An aggregation may only be required for display purposes. Thus, Envision provides a mechanism to perform the aggregation at the tile level, i.e. in-tile aggregation, which is more concise than its regular counterpart. Let’s review a script illustrating how total sales per product can be computed from a table containing the order history:

```envision
table Orders = with
  [| as Product, as OrderDate, as Quantity |]
  [| "banana", date(2020, 4, 14), 5 |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]
  [| "banana", date(2020, 4, 17), 2 |]

show table "Sales by Product" with
  same(Orders.Product) as "Product"
  min(Orders.OrderDate) as "Since"
  sum(Orders.Quantity) as "Sold"
  group by Orders.Product
```

Which displays the following table:

| Product | Since        | Sold |
|---------|--------------|------|
| apple   | Apr 15, 2020 | 10   |
| banana  | Apr 14, 2020 | 7    |
| orange  | Apr 16, 2020 | 2    |

In the script above, the `group by Orders.Product` indicates the chosen grouping for the tile inputs. The aggregator `min()`  and `sum()`  compute the lowest value and the sum of values respectively. Finally, the `same()` aggregator indicates that the grouping is expected to contain identical values, and fail otherwise, and returns one of those values.

This script is equivalent to the alternative script that does not rely on an in-tile aggregation by only group table, as illustrated by:

```envision
table Orders = with
  [| as Product, as OrderDate, as Quantity |]
  [| "banana", date(2020, 4, 14), 5 |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]
  [| "banana", date(2020, 4, 17), 2 |]

table Products[Product] = by Orders.Product
Products.Since = min(Orders.OrderDate)
Products.Sold = sum(Orders.Quantity)

show table "Sales by Product" with
  Product
  Products.Since
  Products.Sold
```

Envision provides a minor syntactic sugar to simplify the first script of this section by removing the `same()` aggregator, as illustrated by:

```envision
table Orders = with
  [| as Product, as OrderDate, as Quantity |]
  [| "banana", date(2020, 4, 14), 5 |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]
  [| "banana", date(2020, 4, 17), 2 |]

show table "Sales by Product" with
  Orders.Product
  min(Orders.OrderDate) as "Since"
  sum(Orders.Quantity) as "Sold"
  group by Orders.Product
```

The script above works because Envision, based on the `group by Orders.Product`, is capable of inferring that `Orders.Product` is a constant for each group and thus doesn’t actually require an aggregation.

Alternatively to the `group by` option there is also a `group into` option, which is akin to the `into` option used for the regular aggregation outside tiles, as illustrated by:

```envision
table Orders = with
  [| as Product, as OrderDate, as Quantity |]
  [| "banana", date(2020, 4, 14), 5 |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]
  [| "banana", date(2020, 4, 17), 2 |]

table Products[Product] = by Orders.Product

show table "Sales by Product" with
  Product
  min(Orders.OrderDate) as "Since"
  sum(Orders.Quantity) as "Sold"
  group into Products
```

The script just above is strictly equivalent to the previous one. It leverages the `group into` syntax to specify the aggregation target for the tile input table.

For the in-tile aggregation, Envision leverages the keyword `group by` and `group into` rather than simply `by` and `into`. This design is not an accident: adding the `group` prefix is used by Envision to differentiate between an aggregation that would occur with the last vector passed as input to the tile and the in-tile aggregation.

Then, at the tile level, it is also possible to order the results, as illustrated by:

```envision
table Orders = with
  [| as Product, as OrderDate, as Quantity |]
  [| "banana", date(2020, 4, 14), 5 |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]
  [| "banana", date(2020, 4, 17), 2 |]

show table "Sales by Product" with
  Orders.Product
  min(Orders.OrderDate) as "Since"
  sum(Orders.Quantity) as "Sold"
  group by Orders.Product
  order by Orders.Product desc
```

Which displays the following table:

| Product | Since        | Sold |
|---------|--------------|------|
| orange  | Apr 16, 2020 | 2    |
| banana  | Apr 14, 2020 | 7    |
| apple   | Apr 15, 2020 | 10   |

The ordering is enforced by the `order by` option, which can optionally be followed by the keyword `desc`, which ensures a _reverse_ ordering.

The `order by` keyword is reminiscent of the `sort` keyword, however there is an important difference between the two. The `order by` is applied _after_ the aggregation, while the `sort` is applied _before_ the aggregation. This implies that `order by` cannot be used to control what happens with order-dependent aggregators like `first()` or `last()`. This also implies that `sort` cannot be used to control the ordering of the results displayed by a tile.

It is also possible to group against multiple vectors, as illustrated by:

```envision
table Orders = with
  [| as Product, as OrderDate, as Quantity |]
  [| "banana", date(2020, 4, 14), 5 |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]
  [| "banana", date(2020, 4, 17), 2 |]

show table "Sales by Product" with
  Orders.Product
  Orders.OrderDate
  sum(Orders.Quantity) as "Sold"
  group by [Orders.Product, Orders.OrderDate]
```

Which displays the following table:

| Product | OrderDate    | Sold |
|---------|--------------|------|
| apple   | Apr 15, 2020 | 3    |
| apple   | Apr 16, 2020 | 7    |
| banana  | Apr 14, 2020 | 5    |
| banana  | Apr 17, 2020 | 2    |
| orange  | Apr 16, 2020 | 2    |

The script aboves aggregates the `Orders` table against a complex dimension `[Orders.Product, Orders.OrderDate]` made of two vectors, instead of the one in the previous script. As a result, both `Orders.Product`  and `Orders.OrderDate` can appear without aggregators among the input vectors of the `table` tile.

Finally, it is also possible to sort against multiple columns as illustrated by:

```envision
table Orders = with
  [| as Product, as OrderDate, as Quantity |]
  [| "banana", date(2020, 4, 14), 5 |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]
  [| "banana", date(2020, 4, 17), 2 |]

show table "Sales by Product" with
  Orders.Product
  Orders.OrderDate
  sum(Orders.Quantity) as "Quantity"
  group by [Orders.Product, Orders.OrderDate]
  order by [sum(Orders.Quantity), Orders.OrderDate] desc
```

Which displays the following table:

| Product | OrderDate    | Sold |
|---------|--------------|------|
| apple   | Apr 16, 2020 | 7    |
| banana  | Apr 14, 2020 | 5    |
| apple   | Apr 15, 2020 | 3    |
| banana  | Apr 17, 2020 | 2    |
| orange  | Apr 16, 2020 | 2    |

In the script above, the ordering is done against an expression `sum(Orders.Quantity)`. Indeed, Envision allows arbitrary expressions to be used as grouping or sorting options for both `group by` and `order by`.
