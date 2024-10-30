+++
title = "Cross tables"
description = ""
weight = 6
+++

A cross table represents the Cartesian product between two tables. Cross tables are typically intended for situations that involve multiple dimensions (e.g. stores and products, SKUs and days, etc). Source tables can broadcast into the cross table. Cross tables also provide an additional class of vector operations within Envision.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Syntax overview

The keyword `cross` is used to declare a cross table as illustrated by:

```envision
table R = extend.range(2)
table S = extend.range(3)

table RS = cross(R, S)
RS.A = R.N
RS.B = S.N

show table "cross" a1b5 with RS.A, RS.B
```

In the above script, the two assignments of `RS.A` and `RS.B`, respectively originating from `R` and `S` work because the table `RS` has `R` and `S` as two upstream tables. The table tile displays the 6=2x3 lines, which result from the Cartesian product between `R` and `S`.

The right source table within a cross should be a [small table](../table-sizes/). This constraint ensures that large cross tables can be processed efficiently when performing complex operations, such as the ones allowed by the `each` keyword.

A cross table has exactly two primary dimensions. Thus, the two source tables must be distinct and have one primary dimension each. The scalar table and cross tables cannot be used as source tables.

Every operation that expects two or more vectors to be in the same table attempts at finding a common table between those vectors. A cross table, once declared, becomes a candidate for being this common table.

For example, a map operation performed between two independent tables operates over the cross table associated to this pair of tables:

```envision
table R = extend.range(2)
table S = extend.range(3)

table RS = cross(R, S)
s = sum((1 into R) + (1 into S))

show scalar "sum" with s // 12
```

In the above script, the sum `(1 into R) + (1 into S)` is broadcasted in the common table between `R` and `S`, that is, the cross table `RS`.  The resulting value, `2` over all the lines of the table `RS` is finally summed into `s`, a scalar variable.

The table `RS` must be declared for the above script to work. Indeed, Envision adopts a defensive design where combining within a single map operation two unrelated tables is illegal - unless the corresponding cross table is explicitly declared. This behavior prevents the accidental, and likely nonsensical, combination of values originating from unrelated tables.

A similar effect is obtained beyond the map operations, for example:

```envision
table R = extend.range(2)
table S = extend.range(3)
table RS = cross(R, S)
c = sum(sum(1) by [R.N, S.N]) // RS as common table
show scalar "count" with c // 6
````

Or alternatively:

```envision
table R = extend.range(2)
table S = extend.range(3)
table RS = cross(R, S)
show table "cross" a1b6 with R.N, S.N // RS as common table
```

A cross table can be aggregated into its source tables:

```envision
table R = extend.range(2)
table S = extend.range(3)

table RS = cross(R, S)
RS.A = R.N
RS.B = S.N

R.C = sum(RS.A + RS.B)
S.D = sum(RS.A + RS.B)

show table "R" a1b5 with R.C
show table "S" c1d5 with S.D
```

In the above script, `R.C` (resp. `S.D`) is defined as an aggregation from the table `RS` to the table `R` (resp. `S`).

**Advanced remark**: Cross tables in Envision can be seen as a stepping stone toward an extensive tensor comprehension. The tensor comprehension paradigm is the descendent of the array programming paradigm.

**Roadmap:** Cross tables are limited to two source tables, however we plan to lift this limitation in the future.

### Transposition

It is not possible to declare two cross tables that have the same dimensions _in the same order_.  However, as the ordering of the source dimensions matters, it is possible to declare two cross tables that have the same source dimensions, but in a distinct order. It is also possible to broadcast a cross table into its transposed counterpart.

Let’s consider a transposed cross table:

```envision
table R = extend.range(3)
table S = extend.range(4)

table RS = cross(R, S)
table SR = cross(S, R)

RS.N = (R.N into RS) + S.N
SR.N = (R.N into SR) + S.N

show table "" a1d6 with R.N as "R", S.N as "S", RS.N as "RS", SR.N as "SR"
```

In the above script, the variable `R.N` is explicitly broadcast first into the table `RS` and second into the table `SR` because there are two candidate common tables between `R` and `S`: both `RS` and `SR` are eligible. The broadcast indicates to Envision which cross table should be picked.

Indeed, the more direct approach does not compile:

```envision
table R = extend.range(3)
table S = extend.range(4)

table RS = cross(R, S)
table SR = cross(S, R)

RS.N = R.N + S.N // WRONG! Ambiguous common table between RS and SR
```

Simple assignments between a cross table and its transposed cross table are supported. As a result, the previous script can be rewritten as:

```envision
table R = extend.range(3)
table S = extend.range(4)

table RS = cross(R, S)
table SR = cross(S, R)

RS.N = (R.N into RS) + S.N
SR.N = RS.N // Transpose!

show table "" a1d6 with R.N as "R", S.N as "S", RS.N as "RS", SR.N as "SR"
```

The assignment `SR.N = RS.N` is a transposition of the values held within the table `RS` into the table `SR`.

As data accesses are vastly more efficient whenever lookups happen through the left table (more on this in the following), if a series of operations have to be performed through “right” lookups, it’s better to transpose the cross table, and then operate via “left” lookups afterward.

## Filtering a cross table

Filtering a cross table is possible, however the filtering process itself removes the ‘cross’ property, as the table does not hold any more a complete Cartesian product of the source tables. Thus, filtering a cross table is performed by explicitly introducing the relevant table:

```envision
table R = extend.range(2)
table S = extend.range(3)

table RS = cross(R, S)
RS.N = R.N + S.N

table RSf = where RS.N > 3
RSf.N = RS.N

show table "RSf" a1b4 with R.N, S.N, RSf.N // only 3 lines
```

In the above script, the table `RSf` is defined as a filtered version of the cross table `RS`. This table inherits the primary dimensions of `RS` but those dimensions as inherited as secondary dimensions. As both `R` and `S` can broadcast into `RSf`, the table `RSf` is identified as the common table for the table tile.

## Filtering a source table

Filtering a source table of a cross table transitively applies a filter on the cross table itself. This filtering pattern is of primary interest because it preserves the ‘cross’ nature of the table:

```envision
table R = extend.range(2)
table S = extend.range(3)

table RS = cross(R, S)

where R.N == 1
  RS.A = R.N
  RS.B = S.N
  show table "cross" a1b5 with RS.A, RS.B
```

In the above script, the source table `R` is filtered, and as a result, the cross table `RS` is also filtered. The table tile displays 3 lines instead of the 6 lines that would be expected if the table `RS` were unfiltered. The table `RS` is ‘cross’ when declared, and it remains ‘cross’ within the filter.

As filtering according to a source table do preserve the ‘cross’ nature of the cross table, all the operations over the cross table which are allowed _outside_ the `where` block remain allowed.

It is also possible to define a cross table within a filtered context:

```envision
table R = extend.range(2)
table S = extend.range(3)

where R.N == 1
  table RS = cross(R, S)
  RS.A = R.N
  RS.B = S.N
  show table "cross" a1b5 with RS.A, RS.B
```

When a cross table is defined in a filtered context, then this cross table is bound to this context. For example, in the above example, using the table `RS` outside, after the end of the `where` block, would not be allowed.

As a filtered declaration of a cross table is strictly scoped to the filtered block, it is possible to define another identically named table after the end of the `where` block, as illustrated with:

```envision
table R = extend.range(2)
table S = extend.range(3)

where R.N == 1
  table RS = cross(R, S)
  RS.A = R.N
  RS.B = S.N
  show table "cross" a1b5 with RS.A, RS.B

table RS = extend.range(3)
show table "alt" c1d5 with RS.N
```

However, this behavior is specific to filtering blocks that _do impact_ the cross table. Indeed, if a cross table is declared within a `where` block that does not impact any of its source tables, then the scope does not apply, and the cross table can be used after the end of the `where` block:

```envision
table R = extend.range(2)
table S = extend.range(3)
table Dummy = extend.range(4)

where Dummy.N == 1
  table RS = cross(R, S)
  RS.A = R.N
  RS.B = S.N

show table "cross" a1b5 with RS.A, RS.B
```

In the above script, the table `RS` is declared within a filtered scope, but this table is accessed after the end of the scope (i.e. the end of the `where` block) because the filter does not touch `RS` or its source tables.

## Transitive broadcasting
<!-- Potential change https://lokad.atlassian.net/browse/LK-8916 Transitive broadcast should work by default -->

Broadcasting into the cross table is possible for any table that can already broadcast into one of the source tables of the broadcast itself. This mechanism is of interest, for example, for situations that involve multiple hierarchical levels. Let’s consider 3 tables `S1`, `S2` and `T` where `T` extends `S2`, as a cross table, and where `S2` extends `S1`. Let’s see how values originating from `S1` can be broadcast into `T`:

```envision
table R = extend.range(2)
table S1 = extend.range(3)
table S2 small 100 = extend.range(S1.N)

table RS2= cross(R, S2)
RS2.A = R.N
RS2.B = S1.N into S2

show table "cross" a1b5 with RS2.A, RS2.B
```

In the above script, the value `S1.N` is first broadcast into the table `S2` via the expression `S1.N into S2` and then, the resulting expression is itself broadcast into `RS2` via the assignment `RS2.B = ..`.

In order to remove the need for expliciting the intermediate broadcast table, i.e. `S2` in the above script, a dimension can be imported into the cross table itself:

```envision
table R = extend.range(2)
table S1[s1] = extend.range(3)
table S2 small 100 = extend.range(S1.N)

table RS2 = cross(R, S2)
RS2.s1 = S2.s1 // same as 's1 into S2'
RS2.A = R.N
RS2.B = S1.N

show table "cross" a1b5 with RS2.A, RS2.B
```

In the above script, once the dimension `s1` has been imported in the cross table `RS2` via `RS2.s1 = s1 into S2`, there is no longer any need to specify `S2` as the intermediate table. This allows the assignment `RS2.B = S1.N`, which involves a direct broadcast from `S1` to `RS2`.

## Lookups

Lookups offer dictionary-like access to vectors by specifying the key associated with the table’s primary dimension. Both regular tables and cross tables support lookups. The lookup over a cross table specifies two keys to identify the line within the table:

```envision
table R[r] = with
  [| as r |]
  [| 1    |]
  [| 2    |]

table S[s] = with
  [| as s |]
  [| 1    |]
  [| 2    |]
  [| 3    |]

table RS = cross(R, S)
RS.N = r + s

n = RS.N[r: 2, s: 3] 

show scalar "n" with n
```

In the above script, two tables `R` and `S` are declared through their respective table comprehensions. Also, `r` (resp. `s`) is the primary dimension of the table `R` (resp. `S`) and is of type `number`. A lookup is performed via the expression `RS.N[r: 2, s: 3]` to extract a single scalar value from the vector `RS.N`. The `r` and `s` prefixes match the names of the source tables’ dimensions `R` and `S` of the cross table `RS`.

The lookup syntax for cross tables is similar to the one used for regular vector lookup. The dimensions are named to lift any ambiguity. While the ordering of the lookup arguments has no impact, It is recommended, for the sake of code clarity, to keep the dimensions in the order of the declaration of the source tables (as done above).

Lookups over vectors are also allowed, as illustrated by:

```envision
table R[r] = with
  [| as r |]
  [| 1    |]
  [| 2    |]

table S[s] = with
  [| as s |]
  [| 1    |]
  [| 2    |]
  [| 3    |]

table RS = cross(R, S)
RS.N = r + s

table U = with 
  [| as I, as J |]
  [| 2,    3    |]
  [| 1,    2    |]
  [| 0,    1    |] // no matching counterpart

U.N = RS.N[r: U.I, s: U.J]

show table "U" a1b4 with U.I, U.J, U.N
```

In the above script, the lookup `RS.N[r: U.I, s: U.J]` is performed over the table `U`, and it attempts to extract one value from the vector `RS.N` for every line of the table `U`. When there is no matching line to be found within the table `RS`, as is the case for the last line of `U`, then the lookup returns the default value for the type, i.e. 0 (zero) here as the type is `number`.

In order to prevent unmatched lookups being  replaced by default values, the `default fail` option can be specified. This can be done by replacing the declaration line for `U.N` by:

```envision-proto
U.N = RS.N[r: U.I, s: U.J] default fail
```

Once this replacement is done, the above script fails as the last line of the table `U` cannot be looked-up with the cross table `RS`.

Lookups are expected to be infrequently needed in Envision. Default vector behaviors should cover most situations. However, lookups offer a greater degree of expressiveness, which can be required to cope with more complex calculations.

**Roadmap:** Lookups are read-only operations; they don’t yet have a _write_ counterpart in Envision, although we plan to support such a write counterpart in the future.

### Partial lookups

If we look at a cross table as a matrix, a partial lookup can be seen as the selection of a column or of a row: given a column (resp. a row) identifier, the column vector (resp. the row vector) is obtained. The lookup is said to be “partial” - as in _partially explicit_ - because one key is provided explicitly while the other key is provided implicitly:

```envision
table R[r] = with
  [| as r |]
  [| 1    |]
  [| 2    |]

table S[s] = with
  [| as s |]
  [| 1    |]
  [| 2    |]
  [| 3    |]

table RS = cross(R, S)
RS.N = r + s

R.N = RS.N[s: 3]
S.N = RS.N[r: 2]

show table "R" a1b5 with R.N
show table "S" c1d5 with S.N
```

In the above script, the table `RS` is a cross between the tables `R` and `S`. The vector `R.N` (resp. the vector `S.N`) is obtained by performing a partial lookup over a line within the `S` table (resp. the `R` table). The explicit key belongs to the scalar table while the implicit one belongs to the table `R` (resp. the `S` table). As a result, the output of the lookup belongs to the table `R` (resp. the table `S`).

The common table used for the pairs of key can be expressed explicitly with a slightly more verbose version of the same script:

```envision
table R[r] = with
  [| as r |]
  [| 1    |]
  [| 2    |]

table S[s] = with
  [| as s |]
  [| 1    |]
  [| 2    |]
  [| 3    |]

table RS = cross(R, S)
RS.N = r + s

R.N = RS.N[s: 3 into R]
S.N = RS.N[r: 2 into S]

show table "R" a1b5 with R.N
show table "S" c1d5 with S.N
```

From another perspective, we could say that the partial lookup is “underspecified”, and returns all the lines that match the constraint expressed by the key.

Performance-wise, a partial lookup over the right dimension is expected to be more efficient than one over the left dimension. In the above example, the calculation of `S.N` (a left partial lookup) is structurally more efficient than the one of `R.N` (a right partial lookup). Unless there is some structural twist involved (e.g. a shift of dimension), the right partial lookup usually involves a matrix transposition operation, while the left partial lookup does not.

**Advanced remark:** The Envision runtime implementation of cross tables can be expected to loosely similar to multidimensional arrays which become quite popular through the `ndarray` object as found in the open source library NumPy. The left partial lookup is more efficient than the right one because it better preserves the locality of the data accesses.
