+++
title = "random.uniform"
+++

## random.uniform() 🡒 number, autodiff pure function

Returns a deviate sampled from a uniform distribution over the segment $[0,1[$.

```envision
table T = extend.range(5)
T.X = random.uniform() // 1 random value for the table
T.Y = each T
  return random.uniform() // 1 random value per line
show table "" a1c5 with T.X, T.Y
```

The function `random.uniform()` does not have any argument, thus, it operates on the `Scalar` table. This behavior
is illustrated with `T.X` in the above script. In order to obtain a distinct deviate for every line of a table, as it
is the case for `T.Y`, an `each` can be used.

## random.uniform(a: number, b: number) 🡒 number, autodiff pure function

Returns a deviate sampled from a uniform distribution over the segment $[a,b[$. The argument `b` must be greater or equal to the argument `a`.

```envision
table T = with
  [| as A, as B |]
  [| 0.0,  0.1  |]
  [| 1.5,  2.0  |]
  [| 5.5,  8.0  |]
  [| 10.0, 11.0 |]

show table "" a1c4 with
  T.A
  T.B
  random.uniform(T.A, T.B)
```

## See also

* [random.negativeBinomial](../random.negativebinomial/)
* [random.normal](../random.normal/)
* [random.poisson](../random.poisson/)
