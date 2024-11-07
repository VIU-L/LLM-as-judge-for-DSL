+++
title = "ranvar.buckets"
+++

<!-- Non-overlapping segments are still to be implemented
https://lokad.atlassian.net/browse/LK-6748  -->

## ranvar.buckets(weight : number, low : number, high : number) 🡒 ranvar, aggregator

Returns a ranvar as specified segment-wise. The first argument is the weight (later normalized as probabilities). The second and third arguments are the _inclusive_ lower and higher boundaries.

Example:

```envision
table T = with
  [| as P, as A, as B, as X |]
  [| 0.4, 0,  1, "a" |]
  [| 0.6, 2,  3, "a" |]
  [| 0.5, 1,  3, "b" |]
  [| 0.5, 5, 10, "b" |]
  [| 1.0, 0, 10, "c" |]

table G[gdim] = by T.X

where T.X != "c"
  show table "" a1b4 with
    gdim
    ranvar.buckets(T.P, T.A, T.B)
    group by gdim
```

If any of those conditions are not respected, the aggregation fails:

* Each weight must be nonnegative.
* The sum of the weights per group must be positive.
* The buckets must not overlap.

This aggregator is the counterpart of `extend.ranvar()`.

Example:

```envision
x = poisson(3)
table G = extend.ranvar(x)
G.P = int(x, G.Min, G.Max)
y = ranvar.buckets(G.P, G.Min, G.Max)
show scalar "Original" a1b3 with x
show scalar "Recomposed" c1d3 with y
```

## See also

* [extend.ranvar](../../def/extend.ranvar/)
