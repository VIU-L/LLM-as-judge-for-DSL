+++
title = "into"
+++

## (T.a : 'a into U) 🡒 U.'a, operator

The reserved keyword `into` broadcasts the expression `T.a` into the table `U`.

Example:

```envision
table T = with
  [| as N |]
  [| 0 |]
  [| 1 |]
  [| 2 |]

x = 42

show table "" a1a3 with
  (x into T)
```
