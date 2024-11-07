+++
title = "nosort"
+++

## `nosort` in `process` definition, contextual keyword

The `nosort` contextual keyword marks a user-defined process as order-independent. Such a process is called without specifying a `sort` or `scan` option. Such a process cannot declare `keep` variables.

```envision
def nosort process mySquaredSum(x : number) with // 'x' is a vector
  y  = sum(x)
  return y^2

table T = extend.range(3)

x = mySquaredSum(T.N) // no 'sort' required here

show scalar "Squared Sum" a1b1 with x // 36
```

Many, but not all, aggregators are built-in `nosort` processes (ex: `sum`, `avg`, `min`, `max`, `stdev`, `stdevp`).

A `nosort` process can only call other `nosort` proccess, either built-in or user-defined.

The intent behind the `nosort` keyword is to allow more performant execution by explicitly removing the order of the input vectors of the process when applicable.

The code above can be rewritten without the `nosort` option as:

```envision
def process mySquaredSum(x : number) with // 'x' is a scalar
  keep y = 0 // state of the process
  y = y + x
  return y^2
 
table T = extend.range(3)
 
x = mySquaredSum(T.N) sort 1 // dummy sort

show scalar "Squared Sum" a1b1 with x // 36
```

In practice, the use of the `nosort` option is expected to be relatively rare in regular Envision code. Its purpose is mostly to mark special functions (aggregators) that are implemented in ways where ordering is provability irrelevant (associativity).
