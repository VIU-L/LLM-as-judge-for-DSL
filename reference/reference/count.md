+++
title = "count"
+++

## count(T.A : bool) 🡒 number, aggregator

Counts the number of Boolean values that are `true`.

```envision
table T = with
  [| as A, as B |]
  [| true,  "a" |]
  [| true,  "a" |]
  [| true,  "b" |]
  [| false, "b" |]
  [| true,  "c" |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    count(T.A)
    group by gdim
```

While the syntactic sugar `T.*` is strictly independent from `count`, this sugar has been introduced with `count` in mind:

```envision
table T = with
  [| as B |]
  [| "a" |]
  [| "a" |]
  [| "b" |]
  [| "b" |]
  [| "c" |]

where T.B != "c"
  show scalar "Line count" with count(T.*) // 4
```
