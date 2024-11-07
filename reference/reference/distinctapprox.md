+++
title = "distinctapprox"
+++

## distinctapprox(T.'a) 🡒 number, aggregator

The aggregator computes an approximation of how many distinct elements there are. Two elements `a` and `b` are considered identical if `a == b`. It is provided as an alternative to [distinct](../distinct/), but with better performance. As a rule of thumb, this aggregator is intended for vectors beyond 1 million elements.

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
    distinctapprox(T.A)
    group by gdim
```

The aggregator `distinctapprox` supports `text` and `number` data types. It returns `0` on empty groups.

_Advanced remark:_ The approximation is based on [HyperLogLog](https://en.wikipedia.org/wiki/HyperLogLog).

### See also

* [distinct](../distinct/).
* [areSame](../../abc/aresame/).
* [same](../../stu/same/).
