+++
title = "random.poisson"
+++

## random.poisson(lambda: number) 🡒 number, pure function

Returns a deviate sampled from a Poisson distribution of mean `lambda`. The argument `lambda` must be non-negative.

```envision
table T = with
  [| as Lambda |]
  [| 0.0 |]
  [| 1.5 |]
  [| 5.5 |]
  [| 10.0 |]

show table "" a1b4 with
  T.Lambda
  random.poisson(T.Lambda)
```

The values returned by the function are always non-negative integers.

## See also

* [random.negativeBinomial](../random.negativebinomial/)
* [random.normal](../random.normal/)
* [random.uniform](../random.uniform/)
