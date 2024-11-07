+++
title = "product"
+++

## product(T.a : number) 🡒 number, autodiff aggregator

The aggregator returns the numerical product of the grouped numbers.

```envision
table T = with
  [| as A, as B |]
  [| 0,   "a"   |]
  [| 0,   "a"   |]
  [| 0,   "b"   |]
  [| 1,   "b"   |]
  [| 1,   "c"   |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    product(T.A)
    group by gdim
```

The aggregator returns `1` on empty groups.

## See also

* [(*) operator](../../_/multiply/).
