+++
title = "loglikelihood.normal"
+++

## loglikelihood.normal(mu : number, sigma : number, x : number) 🡒 number, autodiff pure function

The logarithm of the likelihood of the normal distribution. The first argument is the mean of the normal distribution. The second argument is the standard deviation. It should be greater or equal to 0. The third argument is the observation.

```envision
table T = extend.range(1000)
mu0 = 1
sigma0 = 2

// learn a parametric distribution from observations
T.X = random.normal(mu0 into T, sigma0)
autodiff T with
  params mu auto
  params sigma in [0.001 ..] auto
  return -loglikelihood.normal(mu, sigma, T.X)

show summary "Regressed normal distribution" a1b1 with mu, sigma // 1.03, 1.97
```

The above script illustrates how the log-likelihood be used to regress the corresponding parametric distribution.
