+++
title = "random.binomial"
+++

## random.binomial(p : number) 🡒 boolean, pure function

Draw a sample from a binomial distribution with 1 trial.
Return `true` if a success is hit. The argument `p` is the
probability of success and must be in the interval $[0, 1]$.

```envision
table T = extend.range(5)
T.IsSuccess = random.binomial(0.5 into T)
show table "" a1c5 with T.IsSuccess
```

The function can be used inside an `autodiff` block, however
no gradient flows back through the function.
