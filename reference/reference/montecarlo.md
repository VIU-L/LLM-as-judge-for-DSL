+++
title = "montecarlo"
+++

## `montecarlo` keyword

The keyword `montecarlo` opens a block. The keyword must be followed by a constant scalar number that indicates the number of interations in the block.

```envision
montecarlo 1000 with
  x = random.uniform(-1, 1)
  y = random.uniform(-1, 1)
  inCircle = x^2 + y^2 < 1
  sample approxPi = avg(if inCircle then 4 else 0)
show scalar "π approximation" with approxPi
```

The `montecarlo` block can be nested with an `each` block.

```envision
table T = with 
  [| 0.1 as ZeroInfl |]
  [| 0.3             |]
  [| 0.8             |]

n = 1000

T.R = each T
  montecarlo n with
    x = if random.binomial(T.ZeroInfl) then 0 else random.poisson(5)
    sample r = ranvar(x)
  return r

show table "Zero-inflated Poisson" a1b3 with T.ZeroInfl, T.R
```

The number of interation must be a positive integer.
