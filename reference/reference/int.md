+++
title = "int"
+++

## int(r: ranvar, a: number, b: number) 🡒 number, pure function

Returns the sum of the probabilities over the inclusive segment \[`a`, `b`\].

Example:

```envision
table T = with
  [| as A, as B |]
  [|  -1, -1 |]
  [|  -1,  1 |]
  [|   1,  2 |]
  [|   5, 10 |]

show table "" a1c4 with
  T.A
  T.B
  int(poisson(3), T.A, T.B)
```

## int(z: zedfunc, a: number, b: number) 🡒 number, pure function

Returns the sum of the zedfunc values over the inclusive segment \[`a`, `b`\].

Example:

```envision
table T = with
  [| as A, as B |]
  [|  -1, -1 |]
  [|  -1,  1 |]
  [|   1,  2 |]
  [|   5, 10 |]

z = max(constant(10) - linear(1) * linear(1), 0)

show table "" a1c4 with
  T.A
  T.B
  int(z, T.A, T.B)
```
