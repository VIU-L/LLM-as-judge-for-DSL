+++
title = "Loops and iterations"
description = ""
weight = 6
+++

While the design of Envision intentionally omits _arbitrary_ loops, it does feature multiple mechanisms to iterate. The intent behind this design is to avoid classes of problems associated with arbitrary loops, such as indeterminate termination and/or indeterminate memory consumption.

**Loop blocks** are a feature for repeating arbitrary sets of operations up to 10 times.

**Iteration blocks** are a feature for repeating _complex_ operations over all lines of a table. These are divided into several categories:

* `each` blocks apply the operation independently to every line of the table, thus ensuring good performance through parallelization.
* `each .. scan` blocks apply the operation one line at a time, in the requested order, and can remember data from one line to the next.
* `montecarlo` blocks are intended for complex pseudo-random generators, typically Monte Carlo simulators (as the name suggests). This type of block is detailed in a later section.
* `autodiff` blocks describe a function to minimize for every line, then perform _gradient descent_ to minimize that value. This type of block is detailed in a later section.

Unlike most programming languages, in Envision, explicit loops and iterations are considered as moderately advanced language features. As a rule of thumb, these features should be avoided whenever the same effect can be obtained by leveraging the relational algebra.

**Table of contents**
{{< toc >}}{{< /toc >}}

## `loop` blocks

A `loop` block repeats a block of Envision code. The number of iterations is passed as an integer literal after the `loop` keyword. The value of the integer must be between 2 and 10 (inclusive). The following script illustrates the `loop` block:

```envision
a = 1
loop 3
  b = a + 1
  a = 2 * b
show summary "" with a, b // 22, 11
```

_Advance remark_: The `loop` is similar to a strongly-typed code macro-expansion. Under the hood, the Envision code is being inflated. This explain why Lokad sets a low limit at 10.

Unlike most blocks in Envision, a `loop` block does not involve any scoping. Hence, in the script above, the variable `b` remains accessible after exiting the `loop` block.

This script could have been equivalently written:

```envision
a = 1

b = a + 1 // iteration 1
a = 2 * b
b = a + 1 // iteration 2
a = 2 * b
b = a + 1 // iteration 3
a = 2 * b

show summary "" with a, b // 22, 11
```

Loop blocks cannot include any tile declaration (i.e. `show` blocks), but they can include table declarations under certain conditions, as illustrated by the following example:

```envision
a = 10
b = 0
table T = extend.range(10)
loop 10
  a = a - 1
  table T = where T.N < a
  b = b + sum(T.N)
show summary "" with a, b // 0, 120
```

In the above script, the repeated declarations of the table `T` are valid because they are filters iteratively applied over the same table.

**Roadmap**: the constraints on the `loop` argument will be relaxed to allow a compile-time constant to be used instead of a literal.

### `loop .. partitioned` blocks

The `loop` block can be used to help Envision parallelize its processing when very large tables are involved - typically over 1 billion lines. The following script illustrates this capability:

```envision
table T = extend.range(123) // T is the super-sized table

T.Rank__ = rank() scan T.N
size__ = count(T.*)
T.Part__ = 1 + floor((T.Rank__ - 1) / size__) * 10

T.N2 = 0
loop n in 1 .. 10 
  where T.Part__ == n // 10 independent segments
    T.N2 = T.N ^ 2

show table "" with T.N, T.N2
```

In the above script, the `where` block placed inside the `loop` block partitions the table `T` into 10 independent segments. Those segments can be processed concurrently by Envision as they are logically independent.

The `loop .. partitioned` syntax is a syntactic sugar that streamlines this precise usage of the `loop` keyword by delegating the partitioning logic to the Envision compiler. The keyword `partitioned` is used as follow:

```envision
table T = extend.range(123)

T.N2 = 0
loop 10 partitioned table T
  T.N2 = T.N ^ 2

show table "" with T.N, T.N2
```

The above script is equivalent to the previous script. The table `T` is partitioned into 10 arbitrary segments. The same logic, as found inside the `loop` block, gets independently executed over each segment.

## `each` blocks

The purpose of the `each` block is to extend what can be done via the relational algebra beyond stand-alone expressions. As the name suggests, `each` blocks offer the possibility to repeat a _block_ of independent operations for each line of a table.

An `each` block operates over a table referred to as the **observation table** - named immediately after the `each` keyword - and produces one or more vectors in that table. The following script illustrates the `each` block:

```envision
table Obs = with
  [| as N |]
  [| 1 |]
  [| 2 |]
  [| 3 |]

Obs.Cpy = each Obs
  cpy = Obs.N + 1
  return cpy

show table "" a1b3 with Obs.N, Obs.Cpy
```

However, the script above could be rewritten in a simpler way through the relational algebra with a stand-alone expression:

```envision
table Obs = with
  [| as N |]
  [| 1 |]
  [| 2 |]
  [| 3 |]

Obs.Cpy = Obs.N + 1

show table "" a1b3 with Obs.N, Obs.Cpy
```

As there are no dependencies between operations performed for every line of the observation table, the execution of the `each` block is automatically parallelized by the Envision runtime.

Inside the block, vectors from the observation table can be assigned to scalar variables, while vectors in tables that are unrelated to the observation table can be manipulated as full vectors:

```envision
table Products = with
  [| as Label, as PurchaseQty, as UnitPrice |]
  [| "Hat",    37,             15.00        |]
  [| "Shirt",  112,            55.00        |]

table Discounts = with
  [| as qty, as Discount |]
  [| 1,      0           |]
  [| 10,     0.1         |]
  [| 100,    0.2         |]

Products.Amount = each Products
  Quantity = Products.PurchaseQty
  Discount = last(Discounts.Discount) when(Discounts.Qty <= Quantity) sort Discounts.Qty
  return Products.UnitPrice * (1 - Discount)

show table "" a1c2 with
  Products.Label
  Products.PurchaseQty
  Products.UnitPrice
  Products.Amount
```

In the above example, for each product, the entire table `Discounts` is traversed to find the discount associated with the quantity being purchased. Without `each`, the above logic could be implemented with `cross`:

```envision
table Products = with
  [| as Label, as PurchaseQty, as UnitPrice |]
  [| "Hat",    37,             15.00        |]
  [| "Shirt",  112,            55.00        |]

table Discounts = with
  [| as qty, as Discount |]
  [| 1,      0           |]
  [| 10,     0.1         |]
  [| 100,    0.2         |]

Products.Amount = with
  Products.Discount = last(Discounts.Discount)
    when (Discounts.Qty < Products.PurchaseQty)
    cross (Products, Discounts)
    sort Discounts.Qty
  return Products.UnitPrice * (1 - Products.Discount)

show table "" a1c2 with
  Products.Label
  Products.PurchaseQty
  Products.UnitPrice
  Products.Amount
```

However the `each` block is more readable and more performant than a `cross` aggregation, especially once the logic grows so complex that several `cross` aggregations are required to represent it. It is therefore recommended to use `each` instead of `cross` (this does not apply to `cross .. by .. at`).

If the observation table happens to be the left component of a cross-table, then vectors from that cross-table can also be loaded into the `each` block:

```envision
table Products = with
  [| as Label, as UnitPrice |]
  [| "Hat",    15.00        |]
  [| "Shirt",  55.00        |]

table Colors = with
  [| as Color, as PriceFactor |]
  [| "blue",   1.1            |]
  [| "red",    1.2            |]
  [| "white",  0.9            |]

// 'Products' is the left component of 'Variants'
table Variants = cross(Products, Colors)
Variants.Price = Products.UnitPrice * Colors.PriceFactor

// Must be computed outside of the 'each'
Variants.MedProductPrice = median(Variants.Price) by Products.Label

Products.MedOfMed = each Products
  // Right cross table can import cross table value 
  // when each is performed on the left cross table
  Colors.MedProductPrice = Variants.MedProductPrice
  return median(Colors.MedProductPrice)

show table "" a1c2 with
  Products.Label
  Products.MedOfMed
```

### Table diagram and limitations

The behaviour of tables in an `each` block depends on that table's relationship with the observation table. The tables are classified as follows:

* The **observation table** appears after the `each` keyword. The body of the block is executed once for each line in the observation table.

* An **upstream table** is any table from which one can broadcast (directly or indirectly) into the observation table. Like the observation table, vectors from upstream tables can be assigned to scalars.

* A **downstream table** is any table into which one can broadcast (directly or indirectly) from the observation table.

* A **full table** is any non-cross table that is neither upstream nor downstream from the observation table. Vectors from full tables can be manipulated as full vectors.

* An **upstream-cross table** is any cross table where the left component is either the observation table or an upstream table, and the right component is a full table.

Tables which do not fit any of the above criteria cannot be used in the `each` block.

Also while upstream and downstream tables allow indirect broadcasting, the chain of broadcast must be _unique_ for the table to be available, otherwise the ambiguity is reported as a compilation error.

In order to reliably achieve good performance even for complex operations, an `each` block has several strict limitations:

* Full tables and upstream-cross [tables must be _small_](../relational-algebra/table-sizes/). This allows Envision to keep the complete vectors in-memory.

* Vectors cannot be broadcast or aggregated from one full table into another. Broadcasting from a scalar to a full table is permitted, and so is aggregating from a full table to a scalar.

   | Expression | Allowed? |
   |---|---|
   | `Day.X = X` | Yes |
   | `Day.X = Week.X` | _No_ |
   | `X = sum(Day.X)` | Yes |
   | `Week.X = sum(Day.X)` | _No_ |
   | `Week.X = sum(Week.X) by Week.C` | _No_ |

* By extension, `by`, `cross` or `over` aggregation, or lookups cannot be used.

* Cannot `sort` by a value that was computed during the `each`. However, values from outside the `each` can be used to sort.

* Only maps and aggregations can be used. Functions which operate on full vectors (such as `argfirst`) are not allowed. In particular, `scan` is not supported.

**Roadmap**: Downstream tables cannot currently be used in `each` block, however we intend to make this feature available in the future. The filters `when` and `where` are not supported either but are likely to be supported in the future.

### Exercise

What is the classification of each of those tables in the three `each` blocks below ?

```envision-proto
read ".." as Category[category]
read ".." as Product[sku] expect [category]
read ".." as Channel[channel]
read ".." as Orders expect [channel, sku, date]

table CategoryWeek = cross(Category, Week)
table ProductWeek = cross(Product, Week)
table ChannelWeek = cross(Channel, Week)

Product.X = each Product
  // Here ?

Week.X = each Week
  // Here ? 

Category.X = each Category
  // Here ?
```

#### Answers

| Table | `each Product` | `each Week` | `each Category` |
|---|---|---|---|
| `Product` | Observation | Full | Downstream |
| `Week` | Full | Observation | Full |
| `Category` | Upstream | Full | Observation |
| `Channel` | Full | Full | Full |
| `Orders` | Downstream | Downstream | Downstream |
| `CategoryWeek` | Upstream-Cross | _Unavailable_ | Upstream-Cross |
| `ProductWeek` | Upstream-Cross | _Unavailable_ | _Unavailable_ |
| `ChannelWeek` | _Unavailable_ | _Unavailable_ | _Unavailable_ |

## `each .. scan` blocks

The `each .. scan` blocks allow you to keep values from one iteration to the next. However, this extra capability implies that the Envision runtime can't parallelize the iterations of an `each .. scan` block. Thus, this variant should only be favored when values need to be kept from one iteration to the next. A simple example is given below:

```envision
table Obs = with
  [| as Date,          as Quantity |]
  [| date(2021, 1, 1), 13          |]
  [| date(2021, 2, 1), 11          |]
  [| date(2021, 3, 1), 17          |]
  [| date(2021, 4, 1), 18          |]
  [| date(2021, 5, 1), 16          |]

Best = 0

Obs.BestSoFar = each Obs scan Obs.Date
  keep Best
  NewBest = max(Best, Obs.Quantity)
  Best = NewBest
  return NewBest

show table "" a1b4 with Obs.Date, Obs.BestSoFar
```

In the above script, `scan Obs.Date` specifies the order in which the lines of the observation table are to be traversed. The statement `keep Best` specifies that the variable `Best` must retain its value from one observation line to the next. Finally, `Best = NewBest` assigns a new value to the variable ; it will be the one available on the next observation line.

Lines of the observation table are processed in the ascender order. However, the option `desc` can be used to specify the descending order, as illustrated by:

```envision
table Obs = with
  [| as Date,          as Quantity |]
  [| date(2021, 1, 1), 13          |]
  [| date(2021, 2, 1), 11          |]
  [| date(2021, 3, 1), 17          |]
  [| date(2021, 4, 1), 18          |]
  [| date(2021, 5, 1), 16          |]

Best = 0

Obs.BestSoFar = each Obs scan Obs.Date desc
  keep Best
  NewBest = max(Best, Obs.Quantity)
  Best = NewBest
  return NewBest

show table "" a1b4 with Obs.Date, Obs.BestSoFar
```

The `each .. scan` block comes with a short series of syntactic constraints relative to the `keep` statements. The block requires at least one `keep` statement. All the `keep` statements must be made at the very beginning of the `each .. scan` block. The `keep` statements must refer to variables that have already been defined, prior to the `each .. scan` block. A variable marked with `keep` is modified by the execution of the `each .. scan` block. Its last value remains available after exiting the `each .. scan` block.

`keep` vectors must be [from small tables](../relational-algebra/table-sizes/) in order to be kept in-memory, and must be scalars, full-table or upstream-table vectors.

As a rule of thumb, [user-defined processes](../functions/) should be preferred to `each .. scan` blocks whenever possible. The `each .. scan` block should be used when the logic grows too complex, or involves keeping non-scalar variables.

### Return-less blocks

It may happens that an `each .. block` is introduced for the sole purpose of getting the last value held by a `keep` variable. Thus, the `return` statement may be omitted altogether as illustrated by the following script:

```envision
table Currencies = with
  [| as Code |]
  [| "EUR"   |]
  [| "JPY"   |]
  [| "USD"   |]

Sep = ""
List = ""
each Currencies scan Currencies.Code
  keep Sep
  keep List
  List = "\{List}\{Sep}\{Currencies.Code}"
  Sep = ", "

show scalar "" with List
```

In the above script, the variable `List` is built through iterative concatenations. However, as only the final form is of interest, a return-less `each .. block` is used.

In practice, however, the above script could be rewritten in simpler way leveraging the built-in `join` aggregator as illustrated by:

```envision
table Currencies = with
  [| as Code |]
  [| "EUR"   |]
  [| "JPY"   |]
  [| "USD"   |]

show scalar "" with join(Currencies.Code; ", ") sort Currencies.Code
```

### `auto` ordering in `scan`

The ordering of the `scan` follows the primary dimension of the table being enumerated through the use of the keyword `auto`:

```envision
table T = extend.range(6)
x = 0
T.X = each T scan auto
  keep x
  x = T.N - x
  return x

show table "T" a1b5 with T.N, T.X
```

The above script is logically identical to the one below:

```envision
table T[t] = extend.range(6)
x = 0
T.X = each T scan t
  keep x
  x = T.N - x
  return x

show table "T" a1b5 with T.N, T.X
```

### Any-order blocks

While persisting variables from one line to the next might be needed, the specific ordering might not matter. Envision provides a syntax to deal with those situations as illustrated by:

```envision
table Obs = with
  [| as X |]
  [| 42   |]
  [| 41   |]
  [| 45   |]

myMin = 1B
myMax = -(1B)
each Obs scan Obs.*
  keep myMin
  keep myMax
  myMin = min(myMin, Obs.X)
  myMax = max(myMax, Obs.X)

show summary "" a1b2 with myMin, myMax
```

In the above script, the `scan Values.*` indicates that an arbitrary order is taken.

As a rule of thumb, this feature should be considered as fringe and sparingly used. Indeed, the Envision compiler does not rely on any proof that ordering does not matter. Hence, if accidentally ordering does matter, the ambiguity might be resolved in non-predictable ways by the Envision runtime.

## `each .. when` blocks

Iterations can be filtered. The `each .. when` block only executes its body on lines where the condition specified by `when` is `true`.

```envision
table T = extend.range(5)

s = 0
each T scan auto when T.N mod 2 == 1
  keep s
  s = s + T.N

show scalar "odd sum" with s // 9
```

In the above script, the filter `when  T.N mod 2 == 1` is applied to every line of the table `T`. It filters out every line where `T.N` is even.

The `each .. when` block cannot return a vector, via the keyword `return` as lines would be missing. Instead, variables marked as `keep` must be used to extract information from the iteration.

**Roadmap:** the `when` condition cannot yet reference a variable marked as `keep`. We plan to lift this limitation in the future. This will allow dynamic filtering with regards to the iteration process itself.

## `for .. in ..` blocks (no diagram)

The `for X in T.X` offers a simple iteration mechanism over the values of a specified vector. Unlike `each` blocks, there is no diagram, no observation table, etc. Instead, the iteration repeats for each value `X` in `T.X` with all the tables - including the table `T` - being available in full. Unlike the `loop` block, this mechanism allows to iterate over a large number of values.

```envision
table T = extend.range(3)
table U = by (T.N mod 2) // U is upstream of T

U.X = 0
each T scan T.N
  keep U.X        
  U.X = U.X + T.N // 'U.X' is a scalar here

U.Y = 0
for N in T.N scan T.N
  keep U.Y
  U.Y = U.Y + N   // 'U.Y' is a vector over 'U' here

show summary "each vs each in" a1b1 with
  sum(U.X) as "each"       // '6'
  sum(U.Y) as "each .. in" // '12'
```

The above script illustrates the difference between the `each T` and the `for N in T.N` behavior. Inside the `each T` block, the table `U` (upstream of `T`) exposes only a single line at each iteration. Inside the `for N in T.N` block, the table `U` is present in full at each iteration.

This mechanism allows to cross a table with itself, as illustrated by:

```envision
table T = extend.range(5)

T.S = for N in T.N
  return N * sum(T.N) when (N < T.N)

show table "" a1b5 with T.N, T.S
```

_Advanced remark:_ This "simple" each is similar to the `for` loop in Python and the `foreach` loop in C#.

## Illustration: k-means clustering

The k-means method is a clustering algorithm that partitions the observations into $k$ clusters. It can be implemented in Envision using the `loop` block. The following script illustrates a simple k-means problem with points distributed over the unit circle.

```envision
numberOfClusters = 10
numberOfPoints = 1000

table C = extend.range(numberOfClusters)
table C[c] = by C.N
table enum D[d] = "x", "y"
table T[t] = extend.range(numberOfPoints)

table TD = cross(T, D)
table CD = cross(C, D)
table TC = cross(T, C)

// Randomly generated data
TD.XY = random.uniform(-0.5 into TD, 0.5)
TD.XY = TD.XY / sqrt(sum(TD.XY^2) into T) // unit circle

// Cluster initialization
CD.XY = random.uniform(-0.5 into CD, 0.5)
CD.XY = CD.XY / sqrt(sum(CD.XY^2) into C) // unit circle

loop 10
  // Compute the distance between each observation and each cluster.
  TC.Distance = each T
    C.Distance = sum((CD.XY - TD.XY)^2)
    return C.Distance

  // Find the closest cluster for each observation.
  T.ClosestC = argmin(TC.Distance, TC.c)
  TD.ClosestC = T.ClosestC

  // Update the cluster values to be equal to the average value of its associated observations.
  CD.XY = avg(TD.XY) by [TD.ClosestC, TD.d] at [CD.c, CD.d]

// Display points and centroids
T.X = TD.XY[d:"x"]
T.Y = TD.XY[d:"y"]
C.X = CD.XY[d:"x"]
C.Y = CD.XY[d:"y"]

table U = with
  [| T.X as X, T.Y as Y, true as IsPoint|]
  [| C.X,      C.Y,      false          |]

U.Color = if U.IsPoint then "blue" else "red"
show scatter "Points (blue) and Cendroids (red)" a1d8 with 
  U.X 
  U.Y { color: #[U.Color] }
```
