+++
title = "median"
+++

## median(T.A : 'a)  🡒 'a, aggregator

Returns the median value for the group according ot the canonical ordering for the data type. All the ordered data types are supported.

Example:

```envision
table T = with
  [| as A, as B, as C |]
  [| "b", 2, date(2020, 1, 8)  |]
  [| "c", 1, date(2010, 9, 1)  |]
  [| "a", 0, date(2019, 12, 1) |]

show summary "" a1c1 with
  median(T.A)
  median(T.B)
  median(T.C)
```

When facing an empty group, the default value for the data type is returned.
