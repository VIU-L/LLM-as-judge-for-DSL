+++
title = "join"
+++

## join(T.A : text; S : text) 🡒 text, ordered aggregator

The aggregator returns the resulting concatenation of the text values. It requires an ordering option, either `sort` or `scan`.

Example:

```envision
table T = with
  [| as A, as B |]
  [| "hello", "a" |]
  [| "hello", "a" |]
  [| "hello", "b" |]
  [| "world", "b" |]
  [| "world", "c" |]

table G[gdim] = by T.B
G.S = ";"

where T.B != "c"
  show table "" a1b4 with
    gdim
    join(T.A; G.S) sort T.A
    group by gdim
```

The `sort` option can be applied to any ordered data type.

Beware, text values are limited to 256 characters in Envision.

It would also be possible to re-implement `join` with a user-defined process:

```envision
def process myJoin(a : text; delimiter : text) with
  keep c = ""
  if c == ""
    c = a
  else
    c = "\{c}\{delimiter}\{a}"
  return c
```

### See also

* [concat](../../abc/concat/).
