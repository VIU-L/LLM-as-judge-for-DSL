+++
title = "negativeBinomial"
+++

## negativeBinomial(mu: number, dispersion: number) 🡒 ranvar, pure function

Returns the negative binomial distribution of mean `mu` and of dispersion `d`. The dispersion is the ratio between the variance and the mean: $d = \frac{\sigma^2}{\mu}$. The dispersion should be greater than one.

```envision
table T = with
  [| as Mu, as Dispersion |]
  [|  0.5,  2.0 |]
  [|  1.5,  2.0 |]
  [|  5.5,  2.0 |]
  [|  10.0, 2.0 |]

show table "" a1c4 with
  T.Mu
  T.Dispersion
  negativeBinomial(T.Mu, T.Dispersion)
```

## negativeBinomial(mu: number, dispersion: number, zeroInflation: number) 🡒 ranvar, pure function

Overload of the `negativeBinomial` function, that returns the negative binomial distribution inflated in zero. It is the mixture between a dirac in 0 (with a weight equal to the `zeroInflation`) and the negative binomial of mean `mu` and of dispersion `d` (with a weight equal to `1-zeroInflation`). `zeroInflation` should be in the range $[0, 1]$.

```envision
table T = with
  [| as Mu, as Dispersion, as ZeroInflation |]
  [|  0.5,  2.0, 0.1 |]
  [|  1.5,  2.0, 0.2 |]
  [|  5.5,  2.0, 0.3 |]
  [|  10.0, 2.0, 0.4 |]

show table "" a1c4 with
  T.Mu
  T.Dispersion
  T.ZeroInflation
  negativeBinomial(T.Mu, T.Dispersion, T.ZeroInflation)
```

## See also

* The [negative binomial distribution](https://en.wikipedia.org/wiki/Negative_binomial_distribution).
