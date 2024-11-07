+++
title = "if"
+++

## if .. then .. else .., ternary operator

The ternary operator `if`-`then`-`else` takes a Boolean as first argument, and two identically typed values as second and third arguments. The resulting syntax `if c then a else b` is treated as an expression.

```envision
table T = with
  [| as A, as B, as C |]
  [| 1,    0,    true |]
  [| 2,    3,    false |]
  [| 4,    5,    false |]

show table "" a1d3 with
  T.A
  T.B
  T.C
  if T.C then T.A else T.B
```

In many languages (C, C++, Java, C#, ..), the ternary operator is written `condition ? if_true : if_false`.

A multi-line syntax is also available. The `else` keywords are indented (relative to the first line), and the expressions are further indented (relative to the `else` keywords): 

```envision
a = 42
x = if random.binomial(0.5) then
      a + 1
    else if random.binomial(0.5) then
      a + 2
    else
      a + 3

show scalar "x" with x
```

For aesthetic reasons, it is recommended to align the `else` vertically with the first `if`, though that is not required. 

## if .. else .., branch statement

The `if` statement introduces a branch block within a user-defined function.

```envision
def pure mySwap(x: number, y: number) with
  a = 0
  b = 0
  if x > y
    a = y
    b = x
  else if x == y
    a = x
    b = x
  else
    a = x
    b = y
  return (a, b)

x, y = mySwap(4, 2)

show summary "" a1b1 with x, y
```

It is also possible to place `return` statements within the branches.

```envision
def pure mySwap(x: number, y: number) with
  if x > y
    return (y, x)
  else if x == y
    return (x, x)
  else
    return (x, y)

x, y = mySwap(4, 2)

show summary "" a1b1 with x, y
```

The `if` statement is not allowed outside the declaration of user-defined functions.
