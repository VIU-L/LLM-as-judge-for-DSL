+++
title = "sum"
+++

The sum of all the elements of the group, as if chaining `+` operations.

## sum(T.a : number) 🡒 number, autodiff aggregator

Returns the sum of the numbers of the group.

Example:

```envision
table T = with
  [| as A, as B |]
  [| 0,   "a"   |]
  [| 0.5, "a"   |]
  [| 0,   "b"   |]
  [| 1,   "b"   |]
  [| 1,   "c"   |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    sum(T.A)
    group by gdim
```

The aggregator returns `0` on empty groups.

## sum(T.a : ranvar) 🡒 number, aggregator

Returns the sum of the ranvars of the group.

Example:

```envision
table T = with
  [| as A, as B |]
  [| 0,   "a"   |]
  [| 0.5, "a"   |]
  [| 0,   "b"   |]
  [| 1,   "b"   |]
  [| 1,   "c"   |]

T.R = poisson(T.A)

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    sum(T.R)
    group by gdim
```

The aggregator returns `dirac(0)` on empty groups.

## sum(T.a : zedfunc) 🡒 number, aggregator

Returns the sum of the zedfuncs of the group.

Example:

```envision
table T = with
  [| as A, as B |]
  [| 0,   "a"   |]
  [| 0.5, "a"   |]
  [| 0,   "b"   |]
  [| 1,   "b"   |]
  [| 1,   "c"   |]

T.R = linear(T.A)

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    sum(T.R)
    group by gdim
```

The aggregator returns `constant(0)` on empty groups.

## See also

* [(+) operator](../../_/add/).
