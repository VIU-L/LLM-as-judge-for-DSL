+++
title = "distinct"
+++

## distinct(T.'a) 🡒 number, aggregator

The aggregator indicates how many distinct elements there are. Two elements `a` and `b` are considered identical if `a == b`.

Example:

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
    distinct(T.A)
    group by gdim
```

The aggregator `distinct` supports `boolean`, `date`, `number`, `text` and `enum` types. It returns `0` on empty groups.

The use of `distinct` is **not recommended** for `number` and `text` for large datasets, as this may cause performance problems. If you only need an approximation of the number of distinct values, use [distinctapprox](../distinctapprox/) instead. 

If the number of distinct values is not relevant, so much as whether it is 1 or more than 2, use the much faster [areSame](../../abc/aresame/) instead. 

### See also

* [areSame](../../abc/aresame/).
* [same](../../stu/same/).
* [distinctapprox](../distinctapprox/).
