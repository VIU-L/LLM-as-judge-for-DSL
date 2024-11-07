+++
title = "sort"
+++

## sort, process option

The `sort` option can be applied to any process call.

```envision
table T = with
  [| as Id, as X |]
  [| "a", 3 |]
  [| "b", 1 |]
  [| "c", 4 |]

x = join(T.Id; "|") sort T.X // b|a|c
y = join(T.Id; "|") sort -T.X // c|a|b

show summary "" with x, y
```

Note: the arguments after `;` are used for the initialization of the process at the grouping level.

The `sort` option also works with user-defined processes:

```envision
table T = with
  [| as Id, as X |]
  [| "a", 3 |]
  [| "b", 1 |]
  [| "c", 4 |]

def process myConcat(t : text; init: text) with
  keep c = init
  c = "\{c}\{t}"
  return c

x = myConcat(T.Id; ":") sort T.X // :bac
y = myConcat(T.Id; ":") sort -T.X // :cab

show summary "" with x, y
```
