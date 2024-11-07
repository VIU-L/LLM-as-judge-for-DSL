+++
title = "random.normal"
+++

## random.normal() 🡒 number, autodiff pure function

Returns a deviate sampled from a normal distribution of mean `0` and standard deviation `1`.

```envision
table T = extend.range(5)
T.X = random.normal() // 1 random value for the table
T.Y = each T
  return random.normal() // 1 random value per line
show table "" a1c5 with T.X, T.Y
```

The function `random.normal()` does not have any argument, thus, it operates on the `Scalar` table. This behavior
is illustrated with `T.X` in the above script. In order to obtain a distinct deviate for every line of a table, as it
is the case for `T.Y`, an `each` can be used.

## random.normal(mu: number, sigma: number) 🡒 number, autodiff pure function

Returns a deviate sampled from a normal distribution of mean `mu` and standard deviation `sigma`. The argument `sigma` must be non-negative.

```envision
table T = with
  [| as Mu, as Sigma |]
  [| 0.0,  0.1 |]
  [| 1.5,  1.0 |]
  [| 5.5,  2.0 |]
  [| 10.0, 3.0 |]

show table "" a1c4 with
  T.Mu
  T.Sigma
  random.normal(T.Mu, T.Sigma)
```

## See also

* [random.negativeBinomial](../random.negativebinomial/)
* [random.poisson](../random.poisson/)
* [random.uniform](../random.uniform/)
