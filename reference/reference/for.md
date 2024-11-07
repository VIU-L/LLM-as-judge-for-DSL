+++
title = "for"
+++

## for .. in .. , keyword

The `for X in T.X` offers a simple iteration mechanism over the values of a specified vector. Unlike `each` blocks, there is no diagram, no observation table, etc.

This mechanism allows to cross a table with itself, as illustrated by:

```envision
table T = extend.range(5)

T.S = for N in T.N
  return N * sum(T.N) when (N < T.N)

show table "" a1b5 with T.N, T.S
```

Several tables can be used as long as the common table exists and is unique:

```envision
table T = extend.range(5)
table U[u] = by T.N mod 2

T.S = for tn in T.N, un in u
  return un + tn * sum(T.N) when (tn < T.N)

show table "" a1b5 with T.N, T.S
```
