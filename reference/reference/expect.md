+++
title = "expect"
+++

The keyword `expect` is used in Envision to indicate that a variable abides to a certain rule.

## 'expect table tbl max tblSize', cap on table size

A cap on the size of a table can be enforced at runtime via the `expect` statement:

```envision
n = 500
table T = extend.range(n) // 'T.N' goes from 1 to 50 (inclusive)
expect table T max 100 // the line fails of 'n' is greater than 100
show table "" with T.N // Runtime error: Table 'T' has 500 lines, maximum was 100.
```

Capping the size of a table is frequently done to very distinct reasons in Envision.

* Some Envision capabilities only work with tables below a given limit. The script will not compile until the constraint is acklowledged explicitly in the script. This behavior improves the overall _correctness-by-design_ in mitigating "surprising" shortcomings of Envision on specific operations that are not scalable (for example due to quadratic complexity).
* Sometimes, certain tables are genuinely expected to remain relatively small (ex: the number of locations), and a large number of lines indicates that something went wrong somewhere. Capping the size of the table is useful to stop the process early, closer to the root cause of the problem.

## 'expect T.dim = U.other', add a secondary dimension to a table

A secondary dimension cna be added at runtime to a table:

```envision
table T[id] = with // 'id' is the primary dimension of 'T'
  [| as id |]
  [| "id0" |]
  [| "id1" |]

table U = with
  [| as RefToId, as Variant |]
  [| "id0",      "black"    |]
  [| "id0",      "white"    |]
  [| "id1",      "black"    |]
  [| "id1",      "white"    |]
  [| "id1",      "green"    |]

// Add 'id' as a secondary dimension to table 'U'.
// This line would fail at runtime if there was a 'U.RefToId' value mismatching 'id'.
expect U.id = U.RefToId

show table "Counts the variants" with
  T.id as "Id"
  count(U.*) into T as "Count" // 'U' is upstream of 'T', thus 'U' can be aggregated into 'T'
// Id,Count
// id0,2
// id1,3
```

## 'read path as tbl expect [dim] with', add a secondary dimension via a read

A secondary dimension be declared while reading a table with `expect`. The dimension itself must appear first in another table.

```envision
read "/products.csv" as Products[Id] with // 'Id' is the primary dimension of 'Products'
  Id : text
  Name : text

read "/variants.csv" as Variants expect [Id] with // 'Id' is a secondary dimension of 'Variants'
  Id : text
  Color : text
```

At runtime, Envision will check that all the values `Variants.Id` are found in `Products.Id`. If an unknown identifiier is encountered in `variants.csv`, then the execution of the script will fail.
