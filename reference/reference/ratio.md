+++
title = "ratio"
+++

## ratio(T.a : boolean) 🡒 number, aggregator

Returns the percentage (between 0 and 1) of input values that are `true`.

Example:

```envision
table T = with
  [| as A, as B |]
  [| false, "a"   |]
  [| true,  "a"   |]
  [| false, "b"   |]
  [| true,  "b"   |]
  [| true,  "c"   |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    ratio(T.A)
    group by gdim
```

The aggregator returns `1` on empty groups.

## ratio(T.a : number) 🡒 number, aggregator

Returns the percentage (between 0 and 1) of input values that are non-zero.

Exemple:

```envision
table T = with
  [| as A, as B |]
  [| 0,   "a"   |]
  [| 0.5, "a"   |]
  [| 0,   "b"   |]
  [| 1,   "b"   |]
  [| 1,   "c"   |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    ratio(T.A)
    group by gdim
```

The aggregator returns `1` on empty groups.

## ratio(T.a : text) 🡒 number, aggregator

Returns the percentage (between 0 and 1) of input values that are non-empty.

Example:

```envision
table T = with
  [| as A, as B |]
  [| "",    "a"   |]
  [| "foo", "a"   |]
  [| "",    "b"   |]
  [| "foo", "b"   |]
  [| "foo", "c"   |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    ratio(T.A)
    group by gdim
```

The aggregator returns `1` on empty groups.
