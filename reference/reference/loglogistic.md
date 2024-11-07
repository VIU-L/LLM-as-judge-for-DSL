+++
title = "logLogistic"
+++

<!-- 'loglogistic' is too tolerant to invalid inputs
https://lokad.atlassian.net/browse/LK-6781 -->

## logLogistic(alpha: number, beta: number) 🡒 ranvar, pure function

Returns a probability distribution over $\mathbb{N}$ obtained from the CDF of the log-logistic distribution with:

$$P_{\alpha,\beta}[X = n] =  F(n+1; \alpha,\beta) - F(n; \alpha,\beta) $$

where

$$F(x; \alpha, \beta) = { 1 \over 1+(x/\alpha)^{-\beta} }$$

The arguments `alpha` and `beta` must be positive or the function fails.

Example:

```envision
table T = with
  [| as Alpha, as Beta |]
  [|  0.5,  2.0 |]
  [|  1.5,  2.0 |]
  [|  5.5,  2.0 |]
  [|  10.0, 2.0 |]

show table "" a1c4 with
  T.Alpha
  T.Beta
  logLogistic(T.Alpha, T.Beta)
```

## See also

* The [log-logistic distribution](https://en.wikipedia.org/wiki/Log-logistic_distribution).
