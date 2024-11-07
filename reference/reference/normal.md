+++
title = "normal"
+++

## normal(mu : number, sigma : number) 🡒 ranvar, pure function

Returns the normal distribution of mean `mu` and standard deviation `sigma`. The `sigma` argument must be non-negative.

```envision
table T = with
  [| as Mu, as Sigma |]
  [|  0.1, 0.1 |]
  [|  1.5, 0.5 |]
  [|  5.5, 1.5 |]
  [|  10,  20  |]

show table "" a1e4 with
  T.Mu
  T.Sigma
  normal(T.Mu, T.Sigma)
```

The normal distribution is a continuous distribution, while the ranvar reflects a count distribution. Thus, the ranvar returned by the `normal` function is defined as the integrated probality of the normal distribution over each segment $[n, n +1[$ for every integer $n$.

## See also

* The [Normal distribution](https://en.wikipedia.org/wiki/Normal_distribution).
