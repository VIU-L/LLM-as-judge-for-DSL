+++
title = "min"
+++

## min(T.A : 'a)  🡒 'a, autodiff aggregator

Returns the maximal value for the group according ot the canonical ordering for the data type. All the ordered data types are supported.

```envision
table T = with
  [| as A, as B, as C |]
  [| "b", 2, date(2020, 1, 8)  |]
  [| "c", 1, date(2010, 9, 1)  |]
  [| "a", 0, date(2019, 12, 1) |]

show summary "" a1b4 with
  min(T.A)
  min(dirac(T.B))
  min(T.C)
```

When facing an empty group, the default value for the data type is returned.

## min(n : number, ...) -> number, const autodiff pure function

Returns the smallest of the list of numbers. The function is variadic.

```envision
show scalar "" a1 with min(1, 2)
show scalar "" b1 with min(2, 3, 4)
show scalar "" c1 with min(3, 4, 5, 6)
```

## min(r : ranvar, n : number) -> ranvar, pure function

Same as `min(r, dirac(n))`, see below. The number `n` must be an integer or the function fails.

## min(n : number, r : ranvar) -> ranvar, pure function

Same as `min(dirac(n), r)`, see below. The number `n` must be an integer or the function fails.

## min(r : ranvar, ...) -> ranvar, pure function

If $X_1$ and $X_2$ are two independent random variables over $\mathbb{Z}$ associated to the ranvars `r1` and `r2` respectively, returns $\max(X_1, X_2)$. The function is variadic.

```envision
a = poisson(1)
b = poisson(2)
show scalar "a" a1c3 with a
show scalar "b" a4c6 with b
show scalar "min(a, b)" a7c9 with min(a, b)
show scalar "min(a, b, b)" a10c12 with min(a, a, b)
```

### See also

* [max](../max/)
