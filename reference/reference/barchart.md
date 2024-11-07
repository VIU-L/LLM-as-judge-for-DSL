+++
title = "barchart"
+++

## barchart, tile type

This tile is intended to display a barchart. The expression passed after the `with` keyword should offer an aggregator. An explicit `group by` statement is expected.

```envision
table T = extend.range(10)
T.X = random.poisson(5 into T)
T.G = "G\{T.N}"

show barchart "My Groups" a1b8 {unit: "$"} with
  sum(T.X)
  group by T.G
```

No column options are allowed.
