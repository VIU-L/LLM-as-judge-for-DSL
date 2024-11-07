+++
title = "poisson"
+++

## poisson(lambda: number) 🡒 ranvar, pure function

Returns the Poisson distribution of mean `lambda`.

```envision
table T = with
  [| as Lambda |]
  [|  0.0 |]
  [|  1.5 |]
  [|  5.5 |]
  [|  10.0 |]

show table "" a1b4 with
  T.Lambda
  poisson(T.Lambda)
```

## See also

* The [Poisson distribution](https://en.wikipedia.org/wiki/Poisson_distribution).
