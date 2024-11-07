+++
title = "floor"
+++

## floor(a: number) 🡒 number, const autodiff pure function

Returns the number rounded down to the nearest integer.

```envision
x = 4.2
y = floor(x)
show scalar "" with y
```

The gradient associated to `floor()` is 1, instead of 0, as the mathematical definition would suggest. The purpose of this irregular behavior is to facilate the design of discrete policies.

## See also

* [ceiling](../../abc/ceiling/)
* The [FLOOR.MATH](https://support.office.com/en-us/article/floor-math-function-c302b599-fbdb-4177-ba19-2c2b1249a2f5) function of Excel.
