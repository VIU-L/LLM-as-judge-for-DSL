+++
title = "desc"
+++

## scan [ .. desc], process option

The `desc` keyword is an option for a process call. When `desc` is present, the ordering of the iteration is inverted.

```envision
def process continuedFraction(a: number) with
  keep frac = 1
  frac = a + 1 / frac
  return frac

table T = extend.range(20)

T.Frac = continuedFraction(T.N) scan [T.N desc]

show table "Series" a1b10 with T.N, T.Frac order by T.N
```

When the `scan` takes a tuple, the `desc` option can be indepently applied to every element of the tuple, i.e. `scan [a desc, b, c desc]`.

## order by .. desc, tile option

The `desc` keyword is an option for a table tile block. When `desc` is present, the ordering of the table is inverted.

```envision
table T = with
  [| as X, as Y |]
  [| "a",  3    |]
  [| "b",  2    |]
  [| "c",  1    |]

show table "T" a1b3 with T.X, T.Y order by T.Y desc
```

When the `order by` takes a tuple as argument, the `desc` keyword remains outside the tuple: `order by [a, b, c] desc`. As a tile option, the keyword `desc` does not offer an ordering control over each element that makes the tuple.
