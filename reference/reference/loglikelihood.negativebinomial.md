+++
title = "loglikelihood.negativeBinomial"
+++

## loglikelihood.negativeBinomial(mean : number, dispersion : number, k : number) 🡒 number, autodiff pure function

The logarithm of the likelihood of the negative binomial distribution. The first argument is the mean of the negative binomial distribution. It should be positive. The second argument is the dispersion of the negative binomial. It should be greater or equal to 1. The dispersion $d$ follows the relationship $\sigma^2 = d * \mu$, where $\sigma^2$ is the variance and $\mu$ is the mean. The third argument is the observation. It should be a non-negative integer.

Example:

```envision
table T = extend.range(1000)
mu0 = 1
d0 = 2

// learn a parametric distribution from observations
T.X = random.negativeBinomial(mu0 into T, d0)
autodiff T with
  params mu auto
  params d in [1.01 ..] auto(1.5, 0.1)
  return -loglikelihood.negativeBinomial(mu, d, T.X)

show summary "Regressed negative binomial distribution" a1b1 with mu, d // 1.05, 2.03
```

## loglikelihood.negativeBinomial(mean : number, dispersion : number, zeroInflation, k : number) 🡒 number, autodiff pure function

The logarithm of the likelihood of the zero-inflated negative binomial distribution. The arguments are the same than for the classic negative binomial function, except for the `zeroInflation`, which represents the additional probability in zero. It should be in the range $[0, 1]$.

Example:

```envision
table T = extend.range(1000)
mu0 = 1
d0 = 2
zeroInflation0 = 0.2

// learn a parametric distribution from observations
T.X = random.negativeBinomial(mu0 into T, d0, zeroInflation0)
autodiff T with
  params mu auto
  params d in [1.01 ..] auto(1.5, 0.1)
  params zeroInflation in [0 .. 1] auto (0.5, 0.1)

  return -loglikelihood.negativeBinomial(mu, d, zeroInflation, T.X)

show summary "Regressed negative binomial distribution" a1b1 with mu, d, zeroInflation
```