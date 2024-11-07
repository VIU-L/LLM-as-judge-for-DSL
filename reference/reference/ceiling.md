+++
title = "ceiling"
+++

## ceiling(a: number) 🡒 number, const autodiff pure function

Returns the number rounded up to the nearest integer.

```envision
x = 4.2
y = ceiling(x)
show scalar "" with y
```

The gradient associated to `ceiling()` is 1, instead of 0, as the mathematical definition would suggest. The purpose of this irregular behavior is to facilate the design of discrete policies.

## See also

* [floor](../../def/floor/)
