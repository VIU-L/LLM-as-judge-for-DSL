+++
title = "valueAt"
+++

## valueAt(z: zedfunc, x: number) 🡒 number, pure function

Returns the value of the zedfunc at `x`. If `x` is fractional, then the result is obtained from a linear interpolation of the zedfunc.

Example:

```envision
table T = with
  [| as N |]
  [| 0   |]
  [| 0.5 |]
  [| 1   |]
  [| 1.5 |]
  [| 2   |]

a = max(constant(10) - linear(1) * linear(1), 0)
show scalar "a" a1c3 with a
show table "valueAt(a, _)" a4c8 with
  T.N
  valueAt(a, T.N)
```
