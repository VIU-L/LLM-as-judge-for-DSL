+++
title = "rankd"
+++

## rankd(T.s : 's) by T.g : 'g  🡒 T.rk : number, process

Returns the ranks, starting at 1, of the `T.s` values, in decreasing order, assigning the same rank to all tie-breaks.

Example:

```envision
table T = with
  [| as N, as G |]
  [| 0, "a" |]
  [| 0, "a" |]
  [| 2, "b" |]
  [| 3, "b" |]

T.rk = rankd(T.N) by T.G

show table "" a1c4 with
  T.G
  T.N
  T.rk
```
