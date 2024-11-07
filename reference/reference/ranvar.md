+++
title = "ranvar"
+++

## ranvar, contextual keyword

The word `ranvar` is a contextual keyword of the Envision language. It refers to the primitive data type `ranvar` that represents a probability distribution over $\mathbb{Z}$.

```envision
r = poisson(2)
write Scalar as "/sample/oneranvar.ion" with
  MyRanvar = r
```

followed by

```envision
read "/sample/oneranvar.ion" as T with
  MyRanvar : ranvar

show scalar "" a1b2 with same(T.MyRanvar)
```

## ranvar(T.a : number) 🡒 ranvar, aggregator

Returns the empiric ranvar from the given observations. Let's $y_i$ be the $N$ observations, the empiric probability distribution is defined by:

$$P[X = x] = \frac{1}{N} | \\{ y_i |  y_i = x \\} |$$

```envision
table T = with
  [| as A, as B |]
  [| 1,   "a"   |]
  [| 2,   "a"   |]
  [| 1,   "b"   |]
  [| 2,   "b"   |]
  [| 3,   "c"   |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    ranvar(T.A)
    group by gdim
```

Input numbers are rounded to the nearest integer.

The aggregator returns `dirac(0)` on empty groups.

## ranvar(T.a : number, T.w : number) 🡒 ranvar, aggregator

<!-- zero weights should become acceptable 
https://lokad.atlassian.net/browse/LK-6747 -->

Returns the empiric ranvar from the given observations. Let's $y_i$ be the $N$ observations of respective weights $w_i$, the empiric probability distribution is defined by:

$$P[X = x] = \frac{1}{\sum_{i=1}^N w_i} \sum_{ i | y_i = x} w_i$$

```envision
table T = with
  [| as A, as B, as W |]
  [| 1,   "a", 1.0 |]
  [| 2,   "a", 1.0 |]
  [| 1,   "b", 0.5 |]
  [| 2,   "b", 2.5 |]
  [| 3,   "c", 1.0 |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    ranvar(T.A, T.W)
    group by gdim
```

The aggregator returns `dirac(0)` on empty groups.

## ranvar(T.a : number) 🡒 ranvar, montecarlo accumulator

The accumulator returns the empirical distribution of the observed samples.

```envision
r = poisson(3)
montecarlo 1000 with
  deviate = random.ranvar(r)
  sample r = ranvar(deviate)

show summary "Poisson" with 
  mean(r) // 2.93
  dispersion(r) // 1.00
```

The accumulator also operates over vectors.

```envision
table T = extend.range(5)
T.R = poisson(T.N)
montecarlo 1000 with
  T.Deviate = random.ranvar(T.R)
  sample T.R2 = ranvar(T.Deviate)

show table "Poisson" a1b5 with 
  T.R as "Original"
  T.R2 as "Empirical"
```
