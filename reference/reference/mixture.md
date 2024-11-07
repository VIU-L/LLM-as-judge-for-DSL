+++
title = "mixture"
+++

<!-- mixture should be re-interpreted with weights instead of probabilities
https://lokad.atlassian.net/browse/LK-6746 -->

## mixture(T.R : ranvar) 🡒 ranvar, aggregator

Returns the mixture of ranvars. Let $X_i$ be the list of the $N$ ranvars to be aggregated, the mixture is defined by:

$$P[X = x] = \frac{1}{N} \sum_{i=1}^N P[X_i = x] $$

Example:

```envision
table T = with
  [| as A, as B |]
  [| 0,   "a"   |]
  [| 0.5, "a"   |]
  [| 0.5, "b"   |]
  [| 1,   "b"   |]
  [| 1,   "c"   |]

T.R = poisson(T.A)

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    mixture(T.R)
    group by gdim
```

On empty groups, the ranvar `dirac(0)` is returned.

## mixture(T.r : ranvar, T.w : number) 🡒 ranvar, aggregator

Returns the mixture of ranvars. Let $X_i$ be the list of the $N$ ranvars to be aggregated, and $w_i$ their nonnegative weights, the mixture is defined by:

$$P[X = x] = \frac{1}{\sum_i w_i} \sum_{i=1}^N w_i P[X_i = x] $$

Example:

```envision
table T = with
  [| as A, as B, as W |]
  [| 0,   "a", 0.5 |]
  [| 0.5, "a", 0.5 |]
  [| 0.5, "b", 0.3 |]
  [| 1,   "b", 0.3 |]
  [| 1,   "c", 1.0 |]

T.R = poisson(T.A)

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    mixture(T.R, T.W)
    group by gdim
```

All weights are expected to be nonnegative, the execution will fail.

On empty groups, or on groups where the weight sum is zero, the ranvar `dirac(0)` is returned.

## mixture(r1 : ranvar, p1 : number, r2 : ranvar)  🡒 ranvar, pure function

Same as the `mixture(ranvar, number)` aggregator, with:

* a weight of `p1` for the ranvar `r1`.
* a weight of `1 - p1` for the ranvar `r2`.

Example:

```envision
r1 = poisson(2)
r2 = poisson(3)
show scalar "" a1b2 with mixture(r1, 0.2, r2)
```

## mixture(r1 : ranvar, p1 : number, r2 : ranvar, p2 : number, r3 : ranvar)  🡒 ranvar, pure function

Same as the `mixture(ranvar, number)` aggregator, with:

* a weight of `p1` for the ranvar `r1`.
* a weight of `p2` for the ranvar `r2`.
* a weight of `1 - p1 - p2` for the ranvar `r3`.

Example:

```envision
r1 = poisson(2)
r2 = poisson(3)
r3 = poisson(4)
show scalar "" a1b2 with mixture(r1, 0.2, r2, 0.1, r3)
```

## mixture(r1 : ranvar, p1 : number, r2 : ranvar, p2 : number, r3 : ranvar, p3 : number, r4 : ranvar)  🡒 ranvar, pure function

Same as the `mixture(ranvar, number)` aggregator, with:

* a weight of `p1` for the ranvar `r1`.
* a weight of `p2` for the ranvar `r2`.
* a weight of `p3` for the ranvar `r3`.
* a weight of `1 - p1 - p2 - p3` for the ranvar `r4`.

Example:

```envision
r1 = poisson(2)
r2 = poisson(3)
r3 = poisson(4)
r4 = poisson(5)
show scalar "" a1b2 with mixture(r1, 0.2, r2, 0.1, r3, 0.1, r4)
```
