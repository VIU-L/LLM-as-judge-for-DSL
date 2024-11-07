+++
title = "ranvar.uniform"
+++

## ranvar.uniform(n: number) 🡒 ranvar, pure function

Returns the ranvar represented by the function $k \mapsto \frac{1}{|n| + 1}$ on the segment \[0;n\] (if $n \geq 0$) or \[n;0\] (if $n < 0$) and 0 elsewhere. The function fails on fractional numbers.

Example:

```envision
table T = with
  [| as N |]
  [|  0 |]
  [|  1 |]
  [|  3 |]
  [|  10 |]

show table "" a1b4 with
  T.N
  ranvar.uniform(T.N)
```

## ranvar.uniform(m: number, n: number) 🡒 ranvar, pure function

Returns the ranvar represented by the function $k \mapsto \frac{1}{n + 1 - m}$ on the segment \[m;n\] and 0 elsewhere. We assume that $m < n$, an error is thrown if $m > n$. The function fails on fractional numbers.

Example:

```envision
table T = with
  [| as M, as N |]
  [| -1,  0 |]
  [|  0,  1 |]
  [|  1,  3 |]
  [|  5,  10 |]

show table "" a1b4 with
  T.N
  ranvar.uniform(T.M, T.N)
```
