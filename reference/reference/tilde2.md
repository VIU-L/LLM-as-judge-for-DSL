+++
title = "(~~) uppercase equality operator"
+++

## (text ~~ text) 🡒 boolean, const

Returns the case-insensitive equality check. The expression `(a ~~ b)` where `a` and `b` are text values is defined as `(~a == ~b)`.

Example:

```envision
show scalar "" with "Hello" ~~ "HELLO"
```

## (text !~ text) 🡒 boolean, const

Returns the case-insensitive inequality check. The expression `(a !~ b)` where `a` and `b` are text values is defined as `(~a != ~b)`.

```envision
show scalar "" with "Hello" !~ "HELLO"
```
