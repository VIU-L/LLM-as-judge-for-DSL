+++
title = "max"
+++

## max, contextual keyword in read statement

The option `max` can be specified after the table name in a `read` statement to indicate the inclusive maximum number of lines for the table. If the table size exceeds the threshold, then the script fails.

```envision
read "/sample/products.csv" as Products max 10 with
  Product : text

show table "My Products" a1b3 with Products.Product
```

The option `max` offers the possibility to specify two thresholds. The lower inclusive threshold indicates the maximum number of lines that does not generate a warning. The higher inclusive threshold indicates the maximum number of lines that does not generate an error.

```envision
read "/sample/products.csv" as Products max 2 .. 10 with
  Product : text

show table "My Products" a1b3 with Products.Product
```

The warning threshold is intended to help avoid "slowly creeping" situations and detect that a table has grown too much before it becomes a blocking problem.

## max, contextual keyword in table statement

The option `max` can be specified after the table name in a `table` assignement to indicate the inclusive maximum number of lines for the table. If the table size exceeds the threshold, then the script fails.

```envision
table T max 10 = with
  [| as A |]
  [| "b"  |]
  [| "c"  |]
  [| "a"  |]

show table "" with T.A
```

The option `max` offers the possibility to specify two thresholds. The lower inclusive threshold indicates the maximum number of lines that does not generate a warning. The higher inclusive threshold indicates the maximum number of lines that does not generate an error.

```envision
table T max 2 .. 10 = with
  [| as A |]
  [| "b"  |]
  [| "c"  |]
  [| "a"  |]

show table "" with T.A
```

The warning threshold is intended to help avoid "slowly creeping" situations and detect that a table has grown too much before it becomes a blocking problem.

## max(T.A : 'a)  🡒 'a, autodiff aggregator

Returns the maximal value for the group according ot the canonical ordering for the data type. All the ordered data types are supported.

```envision
table T = with
  [| as A, as B, as C |]
  [| "b", 2, date(2020, 1, 8)  |]
  [| "c", 1, date(2010, 9, 1)  |]
  [| "a", 0, date(2019, 12, 1) |]

show summary "" a1b4 with
  max(T.A)
  max(dirac(T.B))
  max(T.C)
```

On empty groups, the default value for the data type is returned.

## max(variadic n : number) -> number, const autodiff pure function

Returns the largest of the list of numbers. The function is variadic.

```envision
show scalar "" a1 with max(1, 2)
show scalar "" b1 with max(2, 3, 4)
show scalar "" c1 with max(3, 4, 5, 6)
```

## max(r : ranvar, n : number) -> ranvar, pure function

Same as `max(r, dirac(n))`, see below. The number `n` must be an integer or the function fails.

## max(n : number, r : ranvar) -> ranvar, pure function

Same as `max(dirac(n), r)`, see below. The number `n` must be an integer or the function fails.

## max(r : ranvar, ...) -> ranvar, pure function

If $X_1$ and $X_2$ are two independent random variables over $\mathbb{Z}$ represeented by the ranvars `r1` and `r2` respectively, returns $\max(X_1, X_2)$. The function is variadic.

```envision
a = poisson(1)
b = poisson(2)
show scalar "a" a1c3 with a
show scalar "b" a4c6 with b
show scalar "max(a, b)" a7c9 with max(a, b)
show scalar "max(a, b, b)" a10c12 with max(a, a, b)
```

Beware, when ranvars are involved, `max(r1, r2)` is _not_ identical to `max(r1, r2, r2)`.

## max(z : zedfunc, n : number) -> zedfunc, pure function

Same as `max(z, constant(n))`, see below. The number `n` must be an integer or the function fails.

## max(n : number, z : zedfunc) -> zedfunc, pure function

Same as `max(constant(n), z)`, see below. The number `n` must be an integer or the function fails.

## max(variadic z : zedfunc) -> zedfunc, pure function

If $f$ and $g$ are two functions $\mathbb{Z} \to \mathbb{R}$ represented by the zedfuncs `z1` and `z2` respective, returns $x \mapsto f(x) + g(x)$.

```envision
a = constant(0)
b = constant(10) - linear(1) * linear(1)
show scalar "a" a1c3 with a
show scalar "b" a4c6 with b
show scalar "max(a, b)" a7c9 with max(a, b)
show scalar "max(a, b, b)" a10c12 with max(a, a, b)
```

### See also

* [min](../min/)
* [small](../../stu/small/)
