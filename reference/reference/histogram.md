+++
title = "histogram"
+++

## histogram, tile type

This tile is intended to display an histogram. Unlike the `barchart`, the bars of the histogram are vertical. The histogram tile expects only a single numeric vector to be provided as an argument.

```envision
table T = extend.range(1000)
T.X = random.poisson(5 into T)

show histogram "My histogram" a1f4 with T.X
```
