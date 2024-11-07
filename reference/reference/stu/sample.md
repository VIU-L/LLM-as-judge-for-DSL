+++
title = "sample"
+++

## `sample` keyword

The keyword `sample` represents an accumulation process within a `montecarlo` block. The accumulation is relative to the iterations of the `montecarlo` block itself.

```envision
montecarlo 1000 with
  x = random.uniform(-1, 1)
  y = random.uniform(-1, 1)
  inCircle = x^2 + y^2 < 1
  sample approxPi = avg(if inCircle then 4 else 0)
show scalar "π approximation" with approxPi
```

With the `ranvar()` accumulator:

```envision
montecarlo 1000 with
  x = if random.binomial(0.2) then 0 else random.poisson(5)
  sample r = ranvar(x)

show scalar "Zero-inflated Poisson" a1b3  with r
```

At this point, `avg()` and `ranvar()` are the sole accumulators supported by `sample`.
