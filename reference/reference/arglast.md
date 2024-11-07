+++
title = "arglast"
+++

## arglast() 🡒 boolean, process

Returns `true` for the last value of the group according to the ordering. The group is optional. When the group is provided, the function returns `true` once per group.

```envision
table T = with
  [| as N, as G |]
  [| 0, "b" |]
  [| 3, "a" |]
  [| 2, "a" |]
  [| 1, "a" |]

T.A = arglast() sort T.N
T.B = arglast() by T.G sort T.N

show table "" a1c3 with
  T.N
  T.G
  T.A
  T.B
```

### See also

* [argfirst](../argfirst/).
