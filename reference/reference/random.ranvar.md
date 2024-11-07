+++
title = "random.ranvar"
+++

## random.ranvar(r: ranvar) 🡒 number, pure function

Returns a deviate sampled from the distribution associated to a ranvar.

```envision
A = poisson(2)
table T = extend.range(10)
show table "" a1b10 with random.ranvar(A into T)
```
