+++
title = "when"
+++

## when, process option

The process option `when` is used to filter lines from the processed table, before the lines are passed to the Envision process.

```envision
table T = with
  [| as Id, as X |]
  [| "a", 3 |]
  [| "b", 1 |]
  [| "c", 4 |]

// Parenthesis needed on expression '(T.X != 1)' due to operator priorities
x = join(T.Id; "") when (T.X != 1) sort T.X // ac
y = join(T.Id; "") when (T.X <= 3) sort T.X // ba

show summary "" with x, y
```

This option also applies to user-defined processes:

```envision
table T = with
  [| as Id, as X |]
  [| "a", 3 |]
  [| "b", 1 |]
  [| "c", 4 |]

def process mySum(x : number) with
  keep total = 0
  total = total + x
  return total

// 'sort' is still required, even if ordering doesn't matter here
x = mySum(T.X) when (T.Id != "a") sort T.X // 5
y = mySum(T.X) when (T.Id == "c") sort T.X // 4

show summary "" with x, y
```
