+++
title = "percent"
+++

<!-- Negative inputs should be disallowed by 'percent'
https://lokad.atlassian.net/browse/LK-6757 -->

## percent(T.a : number) 🡒 T.b : number, function

Returns $x_{i_0} / \sum_i x_i$ for every $x_{i_0}$ of a collection of $x_i$ number values. The grouping operation is performed against the whole table `T`.

Example:

```envision
table T = with
  [| as A |]
  [| 1 |]
  [| 2 |]
  [| 3 |]

T.B = percent(T.A)

show table "" a1a3 with
  T.B
```

## percent(T.a : number) by T.g : 'g 🡒 T.b : number, function

Returns $x_{i_0} / \sum_i x_i$ for every $x_{i_0}$ of a collection of $x_i$ number values. The grouping operation is performed according to the second argument of `percent` which can be of any data type.

Example:

```envision
table T = with
  [| as A, as G |]
  [| 1, "a" |]
  [| 2, "a" |]
  [| 3, "b" |]

T.B = percent(T.A) by T.G

show table "" a1a3 with
  T.B
```
