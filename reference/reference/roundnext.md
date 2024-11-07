+++
title = "roundNext"
+++

## roundNext(a: number) 🡒 number, const pure function

Rounds a number following 'away from zero' rounding convention - rounds to the next 'integer'). Thus, `roundNext(0.5) == 1` and `roundNext(1.5) == 2`. Rounding numbers is a mathematical operation, rather than a presentational setting.

```envision
table T = with
  [| as N  |]
  [| -0.5 |]
  [|  0.5 |]
  [|  1.5 |]

show table "" a1b3 with
  T.N
  roundNext(T.N)
```
