+++
title = "Filtering"
description = "Filtering a table means identifying the lines that should be kept and those that should be removed. For the readers that are familiar with SQL, the filtering capabilities are those associated with the WHERE keyword. Envision provides several filtering mechanisms, the most notable ones are reviewed below."
weight = 3
+++

Filtering a table means identifying the lines that should be kept and those that should be removed. For the readers that are familiar with SQL, the filtering capabilities are those associated with the `WHERE` keyword. Envision provides several filtering mechanisms, the most notable ones are reviewed below.

**Table of contents**
{{< toc >}}{{< /toc >}}

## `where` blocks

The first filtering mechanism is the `where` block. The keyword `where` is followed by a condition, i.e. an expression that evaluates to the Boolean type. The `where` statement is followed by a block, which requires an extra level of indentation, as illustrated with:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

where Orders.Quantity < 5    // Level 0 of indent
  show table "Products" with // Level 1 of indent!
    Orders.Pid               // Level 2 of indent!
    Orders.OrderDate
    Orders.Quantity
```

This script displays the following table, given below, where (as expected) the second line of the original `Orders` table has been filtered.

| Pid    | OrderDate    | Quantity |
|--------|--------------|----------|
| apple  | Apr 15, 2020 | 3        |
| orange | Apr 16, 2020 | 2        |

The `where` filter is active until the block terminates. The following script adds a second tile _within_ the filtered block, and a third tile _after_ exiting the block:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

where Orders.Quantity < 5
  show table "Products" with
    Orders.Pid
    Orders.OrderDate
    Orders.Quantity

  show scalar "Filtered Total (5)" with  // Level 1 of indent
    sum(Orders.Quantity)                 // Level 2 of indent

show scalar "Unfiltered Total (12)" with // Level 0 of indent
  sum(Orders.Quantity)                   // Level 1 of indent
```

Exiting the (filtering) block is done by decreasing the indent from one level. Thus, the last two tiles display different results. The second tile displays `5` as it operates over the filtered table. The third tile displays `12` as it operates over the unfiltered table.

Any table can be filtered _except_ the scalar table in _general_ circumstances. Indeed, filtering the scalar table would lead to counterintuitive behaviors, not aligned with what practitioners would expect from scalar variables. However, there are situations where even the scalar table can be filtered, most notably user-defined function and `each` blocks, discussed later.

## Nested `where` blocks

For complex filtering strategies, it is possible to use complex Boolean expressions, but Envision also supports nesting `where` blocks. For example, the Boolean expression below that uses an `and` operator:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

where Orders.Quantity >= 0 and Orders.Quantity < 6
  show scalar "Filtered Total (5)" with
    sum(Orders.Quantity)
```

The latter part of this script is strictly equivalent to:

```envision-proto
where Orders.Quantity >= 0                // Level 0 of indent
  where Orders.Quantity < 6               // Level 1 of indent
    show scalar "Filtered Total (5)" with // Level 2 of indent
      sum(Orders.Quantity)
```

Which can even be simplified with:

```envision-proto
where Orders.Quantity >= 0              // Level 0 of indent
where Orders.Quantity < 6               // Level 0 of indent
  show scalar "Filtered Total (5)" with // Level 1 of indent
    sum(Orders.Quantity)
```

As Envision does not require extra indentation when multiple `where` filters are used.

In the example above, opting for a complex Boolean expression or for two `where` statements was an arbitrary choice, however, when several tables are involved, several `where` statements need to be used as well.

## No-nesting filters with `keep where`

It’s not always convenient to introduce an extra level of indentation when filtering data. Thus, Envision provides a keyword modifier `keep` that enforces the filtering until the end of the current scope. For example, when `keep where` is used at the level zero of indentation, the filter applies until the end of the script, as illustrated with:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

keep where Orders.Quantity < 6

show scalar "Filtered Total (5)" with // Level 0 of indent
  sum(Orders.Quantity)
```

However, using `keep where` does not imply that the filter remains active until the end of the script, only the end of the _scope_. For example:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

where Orders.Quantity >= 0                // Level 0 of indent
  keep where Orders.Quantity < 6          // Level 1 of indent

  show scalar "Filtered Total (5)" with   // Level 1 of indent
    sum(Orders.Quantity)

show scalar "Unfiltered Total (12)" with  // Level 0 of indent
  sum(Orders.Quantity)
```

In this script, the scope of the `keep where` filter ends with its own containing scope.

## Suffix inline filters

As filters are ubiquitous in scripts, sometimes there is only a single expression that one seeks to filter. In this situation, Envision offers a more compact syntax as an alternative to the `where` block as illustrated by:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

filtered = sum(Orders.Quantity) where Orders.Quantity < 6

show scalar "Filtered Total (5)" with filtered
```

The `where` is suffixed to the aggregation expression. Aggregators will be revisited later in greater detail, however please note that the suffixed `where` is a pure syntactic sugar replacing the nested `where` blocks. The `where` filter does not directly interact with the aggregator `sum` itself.

This behavior becomes more evident when considering a filtered assignment, as illustrated by:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

Orders.Quantity = 10 where Orders.Quantity == 7

show scalar "Unfiltered Total (15)" with
  sum(Orders.Quantity)
```

In the script above, the variable `Orders.Quantity` is overwritten with the value `10`, but only for lines that verifies the condition `Orders.Quantity == 7`.

## Inferred filtering

When filtering one table, the _intent_ is frequently to filter other tables as well. For example, if one filters a `Products` table then one would expect that the `Orders` table - where each order line is associated to a given product - to be filtered as well. Envision provides this behavior, as illustrated by the following example :

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products[pid] = by Orders.Pid

where Products.pid == "apple"
  show scalar "Filtered Total (10)" with
      sum(Orders.Quantity)
```

Here above, the filter is applied to the `Products` table - we are spelling out the `Products.pid` variable for the sake of clarity, but the short name `pid` could have been used instead - and yet, as illustrated by the scalar tile below, the `Orders` table gets filtered as well.

Filter inference helps with keeping Envision scripts concise, as a single filter can be used to filter an arbitrary large number of related tables. In particular, as we will see in the section dedicated to calendar elements, this mechanism is particularly useful to select a time range of interest, and get all the tables accordingly filtered time-wise.

## Filtered assignments

Envision preserves all its capabilities when operating under one or several filters. This implies that new variables can be defined and that variables defined prior to the filter scope can be re-assigned. In this section, we clarify what happens when assignments are made within `where`. Let’s revisit an example that we introduced earlier:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

where Orders.Quantity == 7
  Orders.Quantity = 10

show scalar "Unfiltered Total (15)" with
  sum(Orders.Quantity)
```

In the script above, the variable `Orders.Quantity` is defined prior to the `where` block. This variable gets _partially_ overwritten - due to the presence of the filter - and the results remain persistent after exiting the `where` block.

It is also possible to define a new variable in a `where` block, as illustrated by:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

where Orders.Quantity == 7
  Orders.DefinedInBlock = 10
  show table "This works! (10)" with Orders.DefinedInBlock
```

The variable `Orders.DefinedInBlock` is defined within the `where` block, and used within the same block.

However, if we were to attempt using the variable `Orders.DefinedInBlock` outside its originating scope, as done by:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

where Orders.Quantity == 7
  Orders.DefinedInBlock = 10

show table "" with Orders.DefinedInBlock // WRONG! Undefined variable 'Orders.DefinedInBlock'.
```

The script above does not compile in Envision. Indeed, the variable `Orders.DefinedInBlock` has only been defined for a filtered version of the `Orders` table. This variable has no defined values for non-filtered filtered lines, and thus Envision rejects the use of the `Orders.DefinedInBlock` variable at the last line above, considering that this variable is undefined outside its scope.

Nevertheless, this restriction only applies to assignments related to _filtered_ tables. Variables defined with unfiltered tables can be used outside of a `where` scope :

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table Products[pid] = by Orders.Pid

where Orders.Quantity == 7
  Products.DefinedInBlock = 10

show table "This works!" with Products.DefinedInBlock
```

The script above introduces a variable `Products.DefinedInBlock` within the `where` block. However, as this variable belongs to the `Products` table, which remains unfiltered, this variable can be used after exiting the `where` block, as illustrated by the last line of the script.

**Roadmap**: We plan to allow the usage of partially defined variables. For example, this would allow the above variable `Orders.DefinedInBlock` to be used outside of its block. Variables would become nullables with null values on lines that are not defined. However, we do not plan to repeat the mistake that many languages made  regarding null values. Our design will involve some guarding mechanisms to ensure that null values are never actually processed as such.

## Filter tables

A table can be created by filtering another table. This is implicitly what is happening in Envision when a `where` block is used. However, for convenience, within a `where` block the filtered table keeps the name of its original unfiltered parent. Nevertheless, Envision offers the possibility to _name_ a filtered table. This feature is referred to as _filter tables_.

This mechanism is supported by Envision, as illustrated by:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table FewOrders = where Orders.Quantity < 6 // filter table

show table "Values 3 and 2" with FewOrders.Quantity
```

The script above does two things of interest. First, the filter table `FewOrders` is declared using two keywords: `table` and `where`. Second, the variable `FewOrders.Quantity` is displayed without ever being explicitly assigned, it’s actually the data originating from `Orders.Quantity`.

When a filter table is created, it copies all the vectors found in its source table. Under the hood however, no actual data copy takes place, it’s a pure referencing mechanism in Envision. Creating a filter table costs no more than introducing a `where` block.

The source table can be broadcast, by default, to any of its filter tables. Thus it is possible to assign values from the source table directly to the filter table, as illustrated with:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table FewOrders = where Orders.Quantity < 6

FewOrders.QuantityBis = Orders.Quantity

show table "Values 3 and 2" with FewOrders.QuantityBis
```

This assignment works because, by construction, every single line of `FewOrders` has exactly one originating line in `Orders`. However, the converse is not true, and thus, some lines in `Orders.Quantity` do not get assigned to anything in `FewOrders.QuantityBis`.

Variables from the original (non-filter) table can be assigned freely to the filter table. However, doing the reverse assignment, from the filter table back to the original table, requires a bit more work. Indeed, as the filter table has fewer lines than its original counterpart, Envision must be told what value to use when the value is missing. This process is illustrated in:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table FewOrders = where Orders.Quantity < 6

FewOrders.Quantity = 12

Orders.Quantity = whichever(FewOrders.Quantity) default Orders.Quantity

show table "Updated values" with
  Orders.Pid
  Orders.OrderDate
  Orders.Quantity
```

The displayed tile table is:

| Pid    | OrderDate    | Quantity |
|--------|--------------|----------|
| apple  | Apr 15, 2020 | 12       |
| apple  | Apr 16, 2020 | 7        |
| orange | Apr 16, 2020 | 12       |

This script diverges from the previous one. The variable `FewOrders.Quantity` is defined with a number literal, which gets broadcast to all the lines of the table `FewOrders`. Then, `Orders.Quantity` is overwritten using either the line from `FewOrders` when it exists or the original `Orders.Quantity` value otherwise.

The keyword `whichever` is an Envision aggregator to be detailed later. For now, suffice to say that `whichever` returns any matching value found in the `FewOrders` table (at most one value in the present example, so there isn’t any ambiguity) with a fallback value specified as `Orders.Quantity` if no matching value is found.

Also, it is possible to declare a filter table _within_ a filtered scope, that is, within a `where` block. In this case, the ambient filters are applied to the filter table. For example, the script above is strictly equivalent to the following:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

where Orders.Quantity < 6
  table FewOrders = where true into Orders

FewOrders.Quantity = 12

Orders.Quantity = whichever(FewOrders.Quantity) default Orders.Quantity

show table "Updated values" with
  Orders.Pid
  Orders.OrderDate
  Orders.Quantity
```

The script above leverages an explicit broadcast (as seen previously) with the keyword `into` as it’s the `Orders` table that we seek to filter, not the `Scalar` one. The Boolean literal `true` belongs like all literals to the `Scalar` table.

## Clone tables

A _clone table_ is a special case of filter table, where no line has actually been filtered. This feature is intended as a scoping mechanism when writing Envision scripts. Working over a cloned table ensures that all its vectors remain contained _in this cloned tabled_ without polluting the namespace of the source table. This can be handy when dealing with complex situations and avoid accidental reuse of, for example, very short names introduced for the sake of readability when dealing with complex mathematical expressions.

The canonical syntax to create a clone table is illustrated by:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table CloneOrders = where Orders.*

show table "Cloned!" with
  CloneOrders.Pid
  CloneOrders.OrderDate
  CloneOrders.Quantity
```

The `where Orders.*` is a syntactic sugar to replace `Orders.true` (this shorthand can be used anywhere). This script can also be rewritten in the slightly more verbose but equivalent syntax:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table CloneOrders = where true into Orders

show table "Cloned!" with
  CloneOrders.Pid
  CloneOrders.OrderDate
  CloneOrders.Quantity
```

However, we recommend to preferably use the `where Orders.*` syntax when the intent is to clone a table for the sake of clarity.

## Filter inference on filter tables

As detailed previously, Envision has a filter inference that propagates the effect of a filter from a table to its related tables. This mechanism also applies to filter tables. For example:

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 4, 15), 3 |]
  [| "apple",  date(2020, 4, 16), 7 |]
  [| "orange", date(2020, 4, 16), 2 |]

table CloneOrders = where Orders.*

where Orders.Quantity < 6
  show table "Filtered!" with
    CloneOrders.Pid
    CloneOrders.OrderDate
    CloneOrders.Quantity
```

Which displays:

| Pid    | OrderDate    | Quantity |
|--------|--------------|----------|
| apple  | Apr 16, 2020 | 3        |
| orange | Apr 16, 2020 | 2        |

The script above does not explicitly filter the table `CloneOrders` but the table `Orders` instead, and yet, the table `CloneOrders` ends up filtered. This illustrates Envision’s filter inference mechanism. This mechanism applies for all filter tables, not just clone tables.

## `in` operator

While Envision offers mechanisms to set up and enforce natural joins between tables, input data might be partially inconsistent. For example, the order history may refer to product identifiers that don’t exist anymore. In order to support this class of scenarios, Envision offers the operator `in` which allows to check whether the values found in a vector have a counterpart - or not - in another vector.

Let’s illustrate the `in` operator with the following script:

```envision
table Products = with
  [| as Product, as Price |]
  [| "apple",  1.25 |]
  [| "banana", 0.75 |]

table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 8, 15), 3 |]
  [| "apple",  date(2020, 8, 16), 7 |]
  [| "orange", date(2020, 8, 16), 2 |]

where Orders.Pid in Products.Product
  Orders.Amount = Orders.Quantity * single(Products.Price) \
                                    by Products.Product at Orders.Pid
  show table "Orders" a1c3 with
    Orders.Pid
    Orders.OrderDate
    Orders.Amount
```

The resulting table gets displayed:

| product | OrderDate    | Amount |
|---------|--------------|--------|
| apple   | Aug 15, 2020 | 3.75   |
| apple   | Aug 16, 2020 | 8.75   |

In the above script, the expression `Orders.Pid in Products.Product` results in a Boolean vector associated with the table `Orders` which is `true` if the value of the line is found in the vector `Products.Product`.

It would also have been possible to instead write:

```envision-proto
Orders.Amount = Orders.Quantity * single(Products.Price) \
                                  by Products.Product at Orders.Pid
where Orders.Pid in Products.Product
  show table "Orders" a1c3 with
    Orders.Pid
    Orders.OrderDate
    Orders.Amount
```

However, the computation of `Orders.Amount` takes the needless risk of defaulting when facing empty groups. Placing the definition `Orders.Amount` within the block filtered via the `in` operator ensures that this problem does not happen.

## Filtered dimension assignment

The approach outlined by the `in` operator can be refined further with regards of the dimensions and of the natural joins that exist between tables. This syntax, and its alternatives, is rediscussed in greater details in the section about [secondary dimensions](../secondary-dimensions/). Let’s illustrate this operation with the following script, revising the one of the previous section, that creates a natural join between two initially independent tables:

```envision
table Products[product] = with
  [| as Product, as Price |]
  [| "apple",  1.25 |]
  [| "banana", 0.75 |]

table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2020, 8, 15), 3 |]
  [| "apple",  date(2020, 8, 16), 7 |]
  [| "orange", date(2020, 8, 16), 2 |]

where Orders.product = Orders.Pid
  Orders.Amount = Products.Price * Orders.Quantity
  show table "Orders" a1c3 with
    product
    Orders.OrderDate
    Orders.Amount
```

The resulting table gets displayed:

| product | OrderDate    | Amount |
|---------|--------------|--------|
| apple   | Aug 15, 2020 | 3.75   |
| apple   | Aug 16, 2020 | 8.75   |

In the above script, the expression `Orders.product = Orders.Pid` results in:

* a Boolean vector associated with the table `Orders` which is `true` if the value of the line is found in the vector `product` - just like the `in` operator.
* the association of `product` as a foreign dimension to the filtered table `Orders`. This allows the later calculation of `Orders.Amount` without `by/at`.

In particular, it would not have been possible to instead write:

```envision-proto
Orders.Amount = Products.Price * Orders.Quantity // WRONG!
where Orders.product = Orders.Pid
  show table "Orders" a1c3 with
    product
    Orders.OrderDate
    Orders.Amount
```

Indeed, outside the filtered scope, Envision can’t prove that every `Orders.Pid` has a counterpart in `product`. As a matter of fact, this isn’t even the case.

More generally, the filtered assignment offers the possibility to _bind_ a dimension with the vector of another table. The expression `T.dim = T.expr` returns a Boolean vector in `T` where the line is true if and only if the corresponding value in `T.expr` appears anywhere in the entire dimension `dim`. In addition, the foreign dimension `dim` becomes a foreign dimension of the table `T`. It could be later referred as `T.dim`, but the simpler syntax `dim` is prefered.

In a later section, we will see how `read` statements can be used to create tables from input files while setting-up the dimensions and their relationships via the keyword `expect`. However, when dealing with raw input files whose integrity can’t be fully trusted, enforcing relations at the `read` level isn’t practical because the Envision execution stops at the first foreign dimension error encountered - i.e. an `Orders.Pid` value that doesn’t have a counterpart in `product`. Instead, the combination of the `in` operator and of the filtered dimension assignement offer a more flexible approach (but slightly more verbose and slightly less performant as well) that allows to process both correct and incorrect input data.
