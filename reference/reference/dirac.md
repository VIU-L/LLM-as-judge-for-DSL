+++
title = "dirac"
+++

## dirac(n : number) 🡒 ranvar, pure function

Returns a ranvar with a zero probability everywhere, except on `n` where the probability is 1. The function fails if a fractional number is passed as argument.

Example:

```envision
table T = with
  [| as N |]
  [| -1 |]
  [|  0 |]
  [|  1 |]
  [|  2 |]

show table "" a1b4 with
  T.N
  dirac(T.N)
```
