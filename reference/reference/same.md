+++
title = "same"
+++

## same(T.'a) 🡒 'a, aggregator

The aggregator fails if any pair of elements `a` and `b` of the group don't satifies the equality `a == b`. The aggregator returns the sole value of the group.

Example:

```envision
table T = with
  [| as A, as B |]
  [| 0,   "a"   |]
  [| 0,   "a"   |]
  [| 1,   "b"   |]
  [| 1,   "b"   |]
  [| 1,   "c"   |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    same(T.A)
    group by gdim
```

The aggregator `same` succeeds on any empty group, and returns the default value for the given data type.

### See also

* [areSame](../../abc/aresame/).
* [distinct](../../def/distinct/).
