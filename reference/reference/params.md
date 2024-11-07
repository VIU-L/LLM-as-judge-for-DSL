+++
title = "params"
+++

## params, keyword

The keyword `params` is used to declare learnable parameters within an `autodiff` block.

```envision
table P = extend.range(3)
P.X = 5

autodiff Scalar epochs:1000 with
  params P.X in [P.N ..]
  return sum(P.X)

show table "" a1b3 with P.N, P.X // P.X converges to 1, 2, 3
```
