+++
title = "all"
+++

## all, aggregator

```envision
all(bool: boolean): boolean
```

Returns `true` if all the grouped values are `true`, and returns `false` otherwise.

Example:

```envision
table T = with
  [| as A, as B |]
  [| true,  "a" |]
  [| true,  "a" |]
  [| true,  "b" |]
  [| false, "b" |]
  [| true,  "c" |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    all(T.A)
    group by gdim
```

The aggregator returns `false` on empty groups.

## See also

* [any](../any/)
