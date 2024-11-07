+++
title = "random.negativeBinomial"
+++

## random.negativeBinomial(mu: number, d: number) 🡒 number, pure function

Returns a deviate sampled from a negative binomial distribution of mean `mu` and of variance $σ^2 = d * μ$ where `d` is the dispersion. The mean must be non-negative. The dispersion must be greater or equal to 1.

```envision
table T = with
  [| as Mu, as Dispersion |]
  [| 0.0,  1.0 |]
  [| 1.5,  1.1 |]
  [| 5.5,  2.0 |]
  [| 10.0, 3.0 |]

show table "" a1c4 with
  T.Mu
  T.Dispersion
  random.negativeBinomial(T.Mu, T.Dispersion)
```

When the dispersion equals `1`, the function `random.negativeBinomial` is the same as `random.poisson`.

## random.negativeBinomial(mu: number, d: number, zeroInflation: number) 🡒 number, pure function

Overload of the `random.negativeBinomial`, that returns a deviate sampled from a negative binomial distribution inflated in zero. This probability distribution is the mixture between a dirac in 0 (with a weight equal to the `zeroInflation`) and the negative binomial of mean `mu` and of dispersion `d` (with a weight equal to $1-zeroInflation$). `zeroInflation` should be in the range $[0, 1]$.

```envision
table T = with
  [| as Mu, as Dispersion, as ZeroInflation |]
  [| 0.0,  1.0, 0.1 |]
  [| 1.5,  1.1, 0.2 |]
  [| 5.5,  2.0, 0.3 |]
  [| 10.0, 3.0, 0.4 |]

show table "" a1c4 with
  T.Mu
  T.Dispersion
  T.ZeroInflation
  random.negativeBinomial(T.Mu, T.Dispersion, T.ZeroInflation)
```

## See also

* [random.normal](../random.normal/)
* [random.poisson](../random.poisson/)
* [random.uniform](../random.uniform/)
