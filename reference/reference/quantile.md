+++
title = "quantile"
+++

## quantile, function

```envision
def pure quantile(d: ranvar, p: number): number
```

Returns the `p`th quantile of the ranvar `d`; the smallest integer $k$ such that $\mathbf{P}[d \leq k] \geq p$.    

- `d`: the ranvar representing the probability distribution from which to compute the quantile.
- `p`: the quantile to be computed, as a number between 0 and 1.

### Example

```envision
table T = with
  [| as P |]
  [| 0.1  |]
  [| 0.5  |]
  [| 0.75 |]
  [| 0.99 |]
  [| 1    |]

show table "" a1b4 with
  T.P as "P"
  quantile(poisson(3), T.P) as "Quantile"
```

This outputs the following quantile table:

| P | Quantile |
|---|---|
| 0.10 | 1 |
| 0.50 | 3 |
| 0.75 | 4 |
| 0.99 | 8 |
| 1.00 | 12 |

### Remarks

Calling `quantile` with `p`=0 and `p`=1 will return the minimum and maximum of the distribution, respectively.

An example of a use case for `quantile(d, 1)` is to build safeguards on the output `d` of a probabilistic demand forecast, by comparing `quantile(d, 1)` with the maximum consumption ever seen on a time window equal to the forecasting horizon, to check whether there is a risk of overforecast.

### Errors

Calling `quantile` with a parameter `p` outside of $[0, 1]$ is not supported and results in an error message :

> 'quantile(d,p)' : invalid value 2 for p, should be in [0, 1].
