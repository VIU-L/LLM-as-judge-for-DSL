+++
title = "expsmooth"
+++

## expsmooth(src: number, factor: number; init: number) 🡒 number, process

The process `expsmooth` offers an exponential smoothing method.

```envision
table T[t] = extend.range(100)
T.X = random.normal(10.0 into T, 5.0)

T.Smooth = expsmooth(T.X, 0.1; 0) scan t

show plot "" a1d4 with T.N, T.X, T.Smooth
```

### Annex: implementation

The `expsmooth` process could be manually re-implemented as:

```envision
def process expsmooth_bis(src: number, factor: number; init: number) default 0 with
  keep prev = init
  prev = factor * src + (1 - factor) * prev
  return prev
```
