+++
title = "avg"
+++

## avg(T.a : number) 🡒 number, autodiff aggregator

The aggregator returns the numerical average of the grouped numbers.

```envision
table T = with
  [| as A, as B |]
  [| 0,   "a"   |]
  [| 0,   "a"   |]
  [| 0,   "b"   |]
  [| 1,   "b"   |]
  [| 1,   "c"   |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    avg(T.A)
    group by gdim
```

The aggregator returns `0` on empty groups.

## avg(T.a : number) 🡒 number, montecarlo accumulator

The accumulator returns the numerical average of the observed samples.

```envision
r = poisson(3)
montecarlo 1000 with
  deviate = random.ranvar(r)
  sample mean = avg(deviate)

show scalar "Average" with mean // 2.93
```
