+++
title = "cumsum"
+++

## cumsum(n: number) 🡒 number, process

<!-- TODO: [vermorel] cumsum() is an old function from before we had the scan option. Now we use `sum(X) scan Y` instead of the old `cumsum(X) sort Y`. -->
Returns the cumulative sum of the numbers `n` according to the specified ordering. The group is optional. When the group is specified, it is used to perform a local cumulative sum for each group.

Example:

```envision
table T = with
  [| as N, as G |]
  [| 4, "b" |]
  [| 3, "a" |]
  [| 2, "a" |]
  [| 1, "a" |]

T.A = cumsum(T.N) sort T.N
T.B = cumsum(T.N) by T.G sort T.N

show table "" a1c3 with
  T.N
  T.G
  T.A
  T.B
```

While this process is part of the standard library, it could also be manually redefined with a user-defined process:

```envision
def process myCumsum(n : number) with
  keep sum = 0
  sum = sum + n
  return sum
```
