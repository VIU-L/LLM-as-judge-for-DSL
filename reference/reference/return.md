+++
title = "return"
+++

## return (each block), keyword

At the end of an `each` block, the `return` statement specifies the value to be returned.

```envision
table T = extend.range(5)

factorial = 1
T.Factorial = each T scan auto
  keep factorial
  factorial = factorial * T.N
  return factorial

show table "Factorials" a1b5 with T.N, T.Factorial
```

This `return` statement supports tuple values.

```envision
table T = extend.range(5)

sum = 0
factorial = 1
T.Sum, T.Factorial = each T scan auto
  keep sum
  keep factorial
  sum = sum + T.N
  factorial = factorial * T.N
  return (sum, factorial)

show table "Factorials" a1b5 with T.N, T.Sum, T.Factorial
```

## return each, shorthand syntax
<!-- Tuple values not supported yet by 'return each'
https://lokad.atlassian.net/browse/LK-10015 -->
At the end of an `each` block, the `return each` syntax returns a vector value obtained through the execution of the `each` block.

```envision
table AB[ab] = with
  [| as ab |]
  [| "A"   |]
  [| "B"   |]

table XY[xy] = with
  [| as xy |]
  [| "X"   |]
  [| "Y"   |]

table C = cross(AB, XY)
C.AplusB = each AB
  return each XY 
    return concat(ab into Scalar, xy into Scalar)

show table "A+B" a1b6 with C.AplusB, ab, xy
```

In the above script, `return each` is used to return a vector that belongs to the table `XY` for every line of the table `AB`. This script is equivalent the more verbose variant given below:

```envision
table AB[ab] = with
  [| as ab |]
  [| "A"   |]
  [| "B"   |]

table XY[xy] = with
  [| as xy |]
  [| "X"   |]
  [| "Y"   |]

table C = cross(AB, XY)
C.AplusB = each AB
  XY.AplusB = each XY 
    return concat(ab into Scalar, xy into Scalar)
  return XY.AplusB

show table "A+B" a1b6 with C.AplusB, ab, xy
```

## return (autodiff block), keyword

At the end of an `autodiff` block, the `return` statement specifies the loss associated to the step of the stochastic gradient descent. The loss must be a number.

```envision
autodiff Scalar epochs: 500 learningRate: 0.1 with
  params a auto
  s = a * a
  return s

show scalar "" with a // 0.00
```

This `return` statement supports tuple values. However, only the first value gets interpreted as the loss. The other values, after the first, must been numbers too, and are interpreted as metrics for reporting only.

## return (user-defined function), keyword

At the end of a `def` block, the return `statement` specifies the value to be returned by the function or the process.

```envision
def pure square(x : number) with
  return x * x

show scalar "3^2" with square(3) // '9'
```
