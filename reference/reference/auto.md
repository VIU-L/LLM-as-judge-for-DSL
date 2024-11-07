+++
title = "auto"
+++

## `auto` in `scan`, keyword

Within `scan` statement, the keyword `auto` refers implicitely to the primary dimension of the table being enumerated.

```envision
table T = extend.range(6)

x = 0
T.X = each T scan auto
  keep x
  x = T.N - x
  return x

show table "T" a1b5 with T.N, T.X
```

In the above script, `auto` refers to the primary dimension of `T`. This script is logically identical to:

```envision
table T[t] = extend.range(6)

x = 0
T.X = each T scan t
  keep x
  x = T.N - x
  return x

show table "T" a1b5 with T.N, T.X
```

## `auto` in `autodiff`, keyword

Within an `autodiff` block, the keyword `auto` indicates that a parameter is randomly inialized as a normal distribution of mean 1 and of sigma 0.1.

```envision
table T = with
  [| as X, as Y |]
  [| 1, 3.1 |]
  [| 2, 3.9 |]
  [| 3, 5.1 |]
  [| 4, 6.0 |]
 
autodiff T with
  params a auto
  params b auto
  Delta = a * T.X + b - T.Y
  return Delta^2
 
show scalar "Learned" a1c1 with "y ≈ \{a} x + \{b}"
```
