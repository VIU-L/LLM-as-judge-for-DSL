+++
title = "any"
+++

## any(T.a : boolean) 🡒 boolean, aggregator

Returns `true` if any grouped value is `true`, and returns `false` otherwise.

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
    any(T.A)
    group by gdim
```

The aggregator returns `false` on empty groups.

## See also

* [all](../all/)
