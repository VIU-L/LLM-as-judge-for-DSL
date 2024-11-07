+++
title = "last"
+++

## last(T.A : 'a) 🡒 'a, ordered aggregator

The aggregator returns the last value for each group. It requires an ordering option, either `sort` or `scan`.

```envision
table T = with
  [| as A, as B |]
  [| "hello", "a" |]
  [| "hello", "a" |]
  [| "hello", "b" |]
  [| "world", "b" |]
  [| "world", "c" |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    last(T.A) sort T.A
    group by gdim
```

The ordering option can be applied to any ordered data type. When the group is empty, the default value for the data type is used.

### See also

* [first](../../def/first/)
* [whichever](../../vwx/whichever/)
