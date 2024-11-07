+++
title = "diracz"
+++

## diracz(n : number) 🡒 zedfunc, pure function

Returns a zedfunc with a zero value everywhere, except on `n` where the value is 1. The function fails if a fractional number is passed as argument.

Example:

```envision
table T = with
  [| as N |]
  [| -1 |]
  [|  0 |]
  [|  1 |]
  [|  2 |]

show table "" a1c4 with
  T.N
  diracz(T.N)
```
