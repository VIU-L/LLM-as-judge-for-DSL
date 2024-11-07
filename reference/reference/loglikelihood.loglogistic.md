+++
title = "loglikelihood.logLogistic"
+++

## loglikelihood.logLogistic(alpha : number, beta : number, x : number) 🡒 number, autodiff pure function

The logarithm of the likelihood of the loglogistic distribution. The first argument $\alpha$ is the scale of the loglogistic distribution, and also its median. It should be strictly positive. The second argument $\beta$ is the shape of the distribution, and should be strictly positive. The third argument is the observation. It should be strictly positive.

```envision
R = logLogistic(/* alpha */ 80, /* beta */ 4)
table H = extend.range(1000) // 1000 samples
H.Days = random.ranvar(R into H)

alpha, beta = (20, 2) // approximate initialization
autodiff H epochs:5000 with
  params alpha in [0.01 ..]
  params beta in [1.0 ..] // below 1.0, distribution has no finite mean
  return -loglikelihood.logLogistic(alpha, beta, H.Days)

show scalar "Original α=80.0, β=4.0" a1d2 with min(200, R)
show scalar "Learned α=\{alpha}, β=\{beta}" a3d4 with min(200, logLogistic(alpha, beta))
```

## loglikelihood.logLogistic(alpha : number, beta : number, x : number, isLowerBound : boolean) 🡒 number, autodiff pure function

Overload of the `loglikelihood.logLogistic` function. If `isLowerBound` is false, it computes the log-likelihood associated to $x$. If `isLowerBound` is true, it means that $x$ is a lower bound of the actual observation. In this case, the function computes the loglikelihood that the observation is greater than $x$. This overload is useful when one models the duration of an incomplete event (for example, a lead time for an order still not received), since the `isLowerBound` input lets one utilize the information that an event has not occured yet.

```envision
R = logLogistic(/* alpha */ 80, /* beta */ 4)
table H = extend.range(1000) // 1000 samples, 1 per day
H.Days = random.ranvar(R into H)

H.IsComplete = H.Days + H.N <= 1000 // censoring the tail
H.Days = if H.IsComplete then H.Days else 1000 - H.N + 1

alpha, beta = (20, 2) // approximate initialization
autodiff H epochs:100 with
  params alpha in [0.01 ..]
  params beta in [1.0 ..] // below 1.0, distribution has no finite mean
  return -loglikelihood.logLogistic(alpha, beta, H.Days, not H.IsComplete)

show scalar "Original α=80.0, β=4.0" a1d2 with min(200, R)
show scalar "Learned α=\{alpha}, β=\{beta}" a3d4 with min(200, logLogistic(alpha, beta))
```
