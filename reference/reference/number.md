+++
title = "number"
+++

## number, data type

The `number` data type is supported by Envision.

```envision
a = 1.5
b = a + 1 // 2.5
c = b * 2 // 5
d = c / 5 // 1
show summary "" with a, b, c, d
```

This datatype is backed by `float32` values. Envision does not distinguishes between integers and floating-point numbers.

The keyword `number` appears in user-defined functions:

```envision
def pure mse(a : number, b : number) with
  return (a - b)^2

show scalar "" with mse(1.5, 3.5) // 4
```

and in `read` blocks:

```envision
read "/sample.csv" as Sample with
  MyNumber : number
```
