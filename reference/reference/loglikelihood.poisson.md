+++
title = "loglikelihood.poisson"
+++

## loglikelihood.poisson(lambda : number, k : number) 🡒 number, autodiff pure function

The logarithm of the likelihood of the Poisson distribution. The first argument is the mean of the Poisson distribution. It should be positive. The second argument is the observation. It should be a non-negative integer.

Example:

```envision
table T = extend.range(1000)
lambda0 = 2

// learn a parametric distribution from observations
T.X = random.poisson(lambda0 into T)
autodiff T with
  params lambda in [0.0 ..] auto
  return -loglikelihood.poisson(lambda, T.X)

show summary "Regressed Poisson distribution" a1b1 with lambda // 2.03
```
