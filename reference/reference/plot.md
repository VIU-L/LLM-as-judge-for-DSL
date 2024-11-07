+++
title = "plot"
+++

## plot, tile type

The `plot` tile is intended to display a function _f(x)=y_.

```envision
table T = extend.range(400)
T.X = T.N/100 - 1

show plot "My Cosine" a1c3 with T.X, cos(T.X)
```
