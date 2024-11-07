+++
title = "(+) add operator"
+++

## (+ number) 🡒 number, const autodiff

The unary no-op number operator, intended as the counterpart of the unary minus operator.

```envision
x = 3
show scalar "" with +x
```

## (number + number) 🡒 number, const autodiff

The regular addition of numbers.

```envision
x = 3 + 4
show scalar "" with x
```

## (date + number) 🡒 date, const

Adds an integral number of days to a date.

```envision
x = date(2020,8,25) + 12
show scalar "" with x
```

## (number + date) 🡒 date, const

The sum `(n + d)` where `n` is a number and `d` is a date is defined by `(d + n)`.

```envision
x = 12 + date(2020,8,25)
show scalar "" with x
```

## (ranvar + ranvar) 🡒 ranvar

The addition of ranvars, random variables over $\mathbb{Z}$ assumed to be independent.

```envision
x = poisson(3) + poisson(4)
show scalar "" with x
```

Under the hood, a convolution happens. The mean of the resulting ranvar is equal to the sum of the means of the two ranvar operands.

## (zedfunc + zedfunc) 🡒 zedfunc

The addition of zedfuncs, real functions over $\mathbb{Z}$.

```envision
x = linear(2) + linear(-1)
show scalar "" with x
```

## See also

* [sum](../../stu/sum/).
