+++
title = "crps"
+++

## crps(r : ranvar, n : number) 🡒 number, pure function

Returns the [Continuous Ranked Probability Score](https://www.lokad.com/continuous-ranked-probability-score) (CRPS) between a ranvar and an observation. 

```envision
r = poisson(3)
show scalar "" with crps(r, 4)
```

## crps(r1 : ranvar, r2 : ranvar) 🡒 number, pure function

Returns the extended CRPS between two ranvars. We extend the definition of the CRPS to apply between two ranvar. Let $X_1$ and $X_2$ be two random variables. Let $F_1$ and $F_2$ be the cumulative distribution functions (CDF) of $X_1$ and $X_2$ respectively. We define the CRPS between $X_1$ and $X_2$ as:

$CRPS(X_1, X_2) = \int_{-\infty}^{+\infty} (F_1(x) - F_2(x))^2 dx$ 

```envision
r1 = poisson(3)
r2 = poisson(7)
show scalar "" with crps(r1, r2)
```

