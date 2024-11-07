+++
title = "(-) minus operator"
+++

## (- date) 🡒 number, const

Converts the date to a number and then invert its sign.

```envision
x = date(2020, 10, 1)
show scalar "" with -x
```

This operator is primarily intended for specifying the increasing or decreasing order when sorting against `date` value.

## (- number) 🡒 number, const autodiff

The sign inversion of a number.

```envision
x = 3
show scalar "" with -x
```

## (- ranvar) 🡒 ranvar

The reflected random random variable, i.e. $P[x = -X]$.

```envision
x = poisson(3)
show scalar "" with -x
```

## (- zedfunc) 🡒 zedfunc

The inverted function, i.e. $f(-x)$.

```envision
x = linear(3)
show scalar "" with -x
```

## (number - number) 🡒 number, const autodiff

The regular substraction of two numbers.

```envision
x = 3
y = 2
show scalar "" with x - y
```

## (date - date) 🡒 number, const

The substraction of two dates returns the number of days of difference.

```envision
x = date(2020, 11, 25)
y = date(2019,  8, 24)
show scalar "days" with x - y
```

There is no `+` counterpart for a pair of `date` values.

## (date - number) 🡒 date, const

Substracts an integral number of days to a date.

```envision
x = date(2020,8,25) + 12
show scalar "" with x
```

## (ranvar - ranvar) 🡒 ranvar

The substraction of two random independent variables over $\mathbb{Z}$.

```envision
x1 = poisson(5)
x2 = poisson(3)
show scalar "" a1b2 with x1 - x2
```

Under the hood, a convolution happens. The mean of the resulting ranvar is equal to the difference of the means of the two ranvar operands.

## (zedfunc - zedfunc) 🡒 zedfunc

The substraction of two zedfuncs, real functions over $\mathbb{Z}$..

```envision
f = linear(3)
g = linear(2)
show scalar "" a1b2 with f - g
```
