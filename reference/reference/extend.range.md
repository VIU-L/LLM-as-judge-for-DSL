+++
title = "extend.range"
+++

## extend.range(T.n : number) 🡒 U.*, table function

Creates multiple lines for each line of the original table. The resulting table `U` is an extension of the original table `T`. The values `T.n` must be positive integers or the function fails.

In a typical use case, the function creates a "scenario" line for each line/item in a (catalog) table so that you can do computations on each scenario. For example, imagine you have one line for each pair of shoes in your catalog in a table, and you now want to analyze three different scenarios for each pair of shoes; the function will then create three lines instead of one for each pair of shoes in the table `U`, one line for each scenario.

## Formal definition

```envision
table U = extend.range(T.Count)
```

This expects that `T.Count` is a number, and will produce a new table `U` and that contains all primary dimensions of `T` as secondary dimensions (meaning that the lines of `T` and `U` are associated in a way that one can broadcast from `T` into `U` and aggregate from `U` into `T`). The lines in the new table are such that `T.Count == count(U.*)` (meaning: the number of lines of `U` associated with a line of `T` is equal to the value of `T.Count` on that line).

The output table contains a numbering column named `U.N`, such that for each line of `T`, the associated lines of `U` are numbered from `1` to `T.Count` inclusive.

As all `extend` functions, `extend.range()` will only copy the column of the table's primary dimension to the new table - no other columns will be copied.

### Example 1

```envision
table T = with
  [| as A |]
  [| 1 |]
  [| 1 |]
  [| 3 |]

table U = extend.range(T.A)

show table "" a1c6 with
  T.A
  U.N
```

#### Expected output of example 1

Note that in this example, the table `T` does not have a named primary dimension. Even though its primary dimension is copied to `U`, it cannot be accessed by name. Columns in general are not being copied: The `T.A` column will not be copied to the new table `U`; the only column in table `U` will be `U.N`.

We called the `extend.range()` function by passing column `T.A` as its parameter:

```envision
table U = extend.range(T.A)
```

By doing so, we requested to extend the range of the target table `U` with as many lines as the value of the line in column `T.A` indicates: One line for the first line (`1`), one line for the second line (`1`) and three lines for the third line (`3`), where the process will start counting at 1 and then increment up to the value of the original line in `T.A`. Accordingly, we will receive the following output:

| A | N |
|:----:|:----:|
|1|1|
|1|1|
|3|1|
|3|2|
|3|3|

### Example 2

```envision
table T[A] = with
  [| as A |]
  [| 1 |]
  [| 2 |]
  [| 3 |]

table U = extend.range(T.A)

show table "" a1c6 with
  U.A // This column has been implicitly copied by extend.range() from T.A
  U.N
```

#### Expected output of example 2

In this example, the table `T` actually does have a primary dimension `T[A]` and the values in the column `T.A` are now distinct, which is a prerequisite for creating a primary dimension. In these conditions, the `T.A` column will implicitly be copied to the new table `U`. The column `U.N` will be created according to the values of each line in `T.A`:

| A | N |
|:----:|:----:|
|1|1|
|2|1|
|2|2|
|3|1|
|3|2|
|3|3|

### Expected fails

The function `extend.range` fails if:

* it receives a non-integer argument.
* it receives a negative argument (zero is valid).
* it would create more than 1 billion lines.

## See also

* [FIFO inventory method](/library/fifo-inventory-method/)
* [MOQs and other ordering constraints](/library/moqs-and-other-ordering-constraints/)
* [Secondary dimensions](/language/relational-algebra/secondary-dimensions/)
