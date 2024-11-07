+++
title = "random.integer"
+++

<!-- 'random.integer' should validate its inputs
https://lokad.atlassian.net/browse/LK-8719 -->

<!-- 'random.integer' should be eligible for autodiff
https://lokad.atlassian.net/browse/LK-8717 -->

## random.integer(max: number) 🡒 number, pure function

Returns an integer in the segment $[1,max]$ where $max$ is the inclusive upper bound.

```envision
table T = with
  [| as Max |]
  [| 1      |]
  [| 5      |]
  [| 50     |]
  [| 500    |]

T.K = random.integer(T.Max)

show table "" a1b5 with T.Max, T.K
```

The argument of `random.integer` must be greater or equal to 1.

## random.integer(min: number, max: number) 🡒 number, pure function

Returns an integer in the segment $[min,max]$ where $min$ and $max$ are the inclusive lower and upper bound respectively.

```envision
table T = with
  [| as Min, as Max |]
  [| 1,      10     |]
  [| -10,    1      |]
  [| -10,    10     |]

T.K = random.integer(T.Min, T.Max)

show table "" a1b5 with T.Min, T.Max, T.K
```
