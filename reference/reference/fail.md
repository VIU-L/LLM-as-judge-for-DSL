+++
title = "fail"
+++

## fail, keyword

The keyword `fail` prevents Envision from replacing an empty selection by a default value.

It applies to lookups:

```envision
table T[x] = with
  [| as X, as Y |]
  [| "aa", 11   |]
  [| "bb", 12   |]
  [| "cc", 13   |]

a = T.Y["bb"] default fail

show scalar "" with a // displays 12
```

It applies to aggregators:

```envision
table T[x] = with
  [| as X, as Y |]
  [| "aa", 11   |]
  [| "bb", 12   |]
  [| "cc", 13   |]

T.C = same(x) 
  by T.Y at (min(T.Y + 1, 13))
  default fail

show table "" a1b3 with x, T.C
```

It applies to processes:

```envision
table T[x] = with
  [| as X, as Y |]
  [| "aa", 11   |]
  [| "bb", 13   |]
  [| "cc", 12   |]

def process myMax(x : text) with
  keep mm = ""
  mm = max(x, mm)
  return mm

a = myMax(x) default fail sort T.Y

show scalar "" with a
```
