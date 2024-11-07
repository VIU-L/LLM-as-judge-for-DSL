+++
title = "(...) unpacking operator"
+++

## (...) unpacking operator

The triple dot symbol (...) is the unpacking operator. It deconstructs a tuple value into its underlying sequence of elements.

Unpacking can be used in a lookup:

```envision
table T = with
  [| as A, as X, as Y |]
  [| "foo", 0, 1 |]
  [| "bar", 1, 0 |]

table U[u] = by [T.X, T.Y]
U.A = same(T.A)

xy = (1, 0) // packing statement
show scalar "" with U.A[...xy] // unpacking, display 'bar'
```

The unpacking operator is a shorthand for a prior unpacking statement:

```envision
table T = with
  [| as A, as X, as Y |]
  [| "foo", 0, 1 |]
  [| "bar", 1, 0 |]

table U[u] = by [T.X, T.Y]
U.A = same(T.A)

xy = (1, 0) // packing statement
x, y = xy // unpacking statement
show scalar "" with U.A[x, y] //display 'bar'
```

Unpacking can be used when constructing a tuple:

```envision
table T = with
  [| as A, as X, as Y, as Z |]
  [| "foo", 0, 1, 1 |]
  [| "bar", 1, 0, 0 |]

table U[u] = by [T.X, T.Y, T.Z]
U.A = same(T.A)

xy = (1, 0) // packing
xyz = (...xy, 0) // unpacking, then re-packing

show scalar "" with U.A[...xyz] // unpacking, display 'bar'
```

Unpacking can be used in `by` or `at` arguments:

```envision
table T = with
  [| as A, as X, as Y, as Z |]
  [| "foo", 0, 1, 1 |]
  [| "bar", 1, 0, 0 |]

table U = with
  [| as B, as X, as Y, as Z |]
  [| "qux", 1, 0, 0 |]
  [| "baz", 0, 1, 1 |]

xy = (1, 0)

U.C = whichever(T.A) by [...xy, 0]

show table "" a1e2 with U.B, U.X, U.Y, U.Z, U.C
```
