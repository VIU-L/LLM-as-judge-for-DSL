+++
title = "default"
+++

The `default` keyword is used in Envision to define edge-case behaviors of processes or operators.

## `expr1[expr2] default expr3`, lookup behavior on missing key

The `default` option can be applied to lookup to override the behavior of the loopup if the key is not found in the probed table.

```envision
table Products[product] = with
  [| as Product,   as Price |]
  [| "apple",      1.50     |]
  [| "pear",       1.30     |]
  [| "orange",     2.10     |]
  [| "clementine", 2.70     |]
 
missingPrice = Products.Price["banana"] default -1 // 'banana' does not belong to 'product'

show scalar "" with missingPrice // -1
```

## 'proc(expr1) default expr2', process behavior on empty grouping

When calling a process, the most typical processes in Envision being aggregators, the option `default` can optionally be specified to define the behavior of the process over empty grouping.

```envision
table T = with
  [| as N |]
  [| 1    |]
  [| 2    |]
  [| 3    |]

where T.N < 0 // no lines left in 'T'
  // 'sum(T)' is aggregated to the 'Scalar' table
  show scalar "sum" with sum(T.N) default -1 // -1, because of 'default'
```

## 'def process funname(args) default expr with', user-defined process

When introducing a user-defined process, the value to be returned over empty groupings can optionally be specified via the `default` option.

```envision
table T = with
  [| as N |]
  [| 1    |]
  [| 2    |]
  [| 3    |]

def process mySum(x : number) default -1 with // -1 on empty grouping
  keep sum = 0 // state of the process
  sum = sum + x
  return x

where T.N < 0 // no lines left in 'T'
  // 'sort' is mandatory, but here, ordering matters not.
  show scalar "sum" with mySum(T.N) sort 1 // -1 (due to 'mySum' definition)
```

## See also

* [process](../../pqr/process/)
