+++
title = "random.logLogistic"
+++

## random.logLogistic(alpha : number, beta : number) 🡒 number, pure function

Draw a sample from a loglogistic distribution of scale $\alpha$ and shape $\beta$. Both parameters must be strictly positive.

```envision
table T = extend.range(5)
T.Samples = random.logLogistic(0.5 into T, 2)
show table "" a1c5 with T.Samples
```
