+++
title = "areSame"
+++

## areSame(T.A : 'a) 🡒 boolean, aggregator

The aggregator indicates whether any pair of elements `a` and `b` of the group satifies the equality `a == b`.

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
    areSame(T.A)
    group by gdim
```

The aggregator `areSame` supports all the data types. It returns `true` on empty groups.

### See also

* [distinct](../../def/distinct/).
* [same](../../stu/same/).
