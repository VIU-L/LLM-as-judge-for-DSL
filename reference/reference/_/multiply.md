+++
title = "(*) multiply operator and star operator"
+++

## (number * number) 🡒 number, const autodiff

The regular multiplication of two numbers.

```envision
x = 3
y = 2
show scalar "" with x * y
```

## (ranvar * ranvar) 🡒 ranvar

The multiplication of two random independent variables over $\mathbb{Z}$.

```envision
x1 = poisson(5)
x2 = poisson(3)
show scalar "" a1b2 with x1 * x2
```

This operation is also known as the _Dirichlet convolution_. Under the hood, a convolution happens. The mean of the resulting ranvar is equal to the product of the means of the two ranvar operands.

## (zedfunc * zedfunc) 🡒 zedfunc

The multiplication of two zedfuncs, real functions over $\mathbb{Z}$..

Example:

```envision
f = linear(3)
g = linear(2)
show scalar "" a1b2 with f * g
```

## (text * number) 🡒 text

Repeats text a specified number of times. `"ABC" * 3` is `"ABCABCABC"`. An integer is expected.

Example:

```envision
show scalar "" a1c1 with "ABC" * 3
```

## Table.* 🡒 boolean, star operator

The `MyTable.*` syntax is used as a syntactic sugar for `true into MyTable`.

```envision
table T = with
  [| as A  |]
  [| true  |]
  [| false |]
  [| true  |]
 
where T.A
  show scalar "Lines" a1 with count(T.*) // '2'
  // 'T.*' is a syntactic sugar for 'true into T'
  show scalar "Lines" a2 with count(true into T)  // '2'
```

The `T.*` syntactic sugar can be used in isolation, but this sugar is really intended for `count(T.*)`, which is reminiscent of the SQL syntax `SELECT COUNT(*) FROM myTbl`.

## Seelaso

* [product](../../pqr/product/).
* [REPT](https://support.office.com/en-us/article/rept-function-04c4d778-e712-43b4-9c15-d656582bb061) function of Excel.
