+++
title = "process"
+++

The contextual keyword `process` specifies the type of a user-defined function.

## 'def process funname (params) with', process definition
<!-- https://lokad.atlassian.net/browse/LK-12999
'auto' works with 'scan' but not with 'sort' -->
The modifier `process` indicates that the function processes vector arguments while maintaining in internal state.

```envision
table T = with
  [| as N, as X |]
  [| 0,    1    |]
  [| 1,    2    |]
  [| 2,    -1   |]

def process sumOfSquares(x : number) with
  keep sum = 0 // internal state, preserved while 
  sum = sum + x * x
  return sum

T.CumulativeSum = sumOfSquares(T.X) scan T.N // 'scan' returns the whole vector
total = sumOfSquares(T.X) sort T.N // 'sort' only returns the last value

show table "" with T.N, T.X, T.CumulativeSum
// N,X,CumulativeSum
// 0,1,1
// 1,2,5
// 2,-1,6

show scalar "" with total // 6
```

The vector arguments are comma-separated:

```envision
def process sumOfSquares(x : number, y : number) with
  keep sum = initSum // internal state, preserved while 
  sum = sum + x * x + y * y
  return sum
```

The default value returned by the process when the vector arguments are empty (zero lines) is the default value of the datatype. However, this value can be overridden with the `default` keyword:

```envision
table T = with
  [| as N, as X |]
  [| 0,    1    |]

def process sumOfSquares(x : number) default 42 with // default value specified
  keep sum = 0 // internal state, preserved while 
  sum = sum + x * x
  return sum

// Filter 'T' to make it empty
where T.N != 0 // empty table 'T'
  // Dummy sort (ordering does not matter, sum is commutative).
  show scalar "" with sumOfSquares(T.X) sort 1 // 42
```

The initial state can be controlled by passing initialization arguments after a semi-colon (;) delimiter:

```envision
table T = with
  [| as N, as X |]
  [| 0,    1    |]
  [| 1,    2    |]
  [| 2,    -1   |]

def process sumOfSquares(x : number; initSum : number) with
  keep sum = initSum // internal state, preserved while 
  sum = sum + x * x
  return sum

T.CumulativeSum = sumOfSquares(T.X; 3) scan T.N 

show table "" with T.N, T.X, T.CumulativeSum
// N,X,CumulativeSum
// 0,1,4
// 1,2,8
// 2,-1,9
```

It is possible to use multiple vector arguments and multiple initialization arguments:

```envision
def process sumOfSquares(x : number, y : number; initX : number, initY : number) with
  keep sum = initX + initY // internal state, preserved while 
  sum = sum + x * x + y * y
  return sum
```

## See also

* [def](../../def/def/)
* [pure](../../pqr/pure/)
* [User defined functions](../../../language/functions/)
