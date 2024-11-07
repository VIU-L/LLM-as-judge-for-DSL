+++
title = "smooth"
+++

## smooth(r: ranvar) 🡒 ranvar, pure function

Returns a smooth variant of the original ranvar to mitigate the overfitting issue.

```envision
table T = with // observation
  [| as Obs |]
  [| 1 |]
  [| 0 |]
  [| 0 |]
  [| 2 |]

show scalar "ranvar(T.Obs)" a1c3 with ranvar(T.Obs)
show scalar "smooth(ranvar(T.Obs))" a4c6 with smooth(ranvar(T.Obs))
```

This function is typically intended to smooth ranvars produced through the `ranvar` aggregators over a handfew observations, and mitigate the most obvious artefacts caused by the limited set of observations.

The `smooth` function replaces the original `ranvar` by a mixture distribution made of Poisson distributions: each histogram bucket is replaced with a Poisson distribution of mean equal to the index of the bucket, and of weight equal to the weigth of the bucket.

If the bucket index is negative, then the absolute value of the bucket index is used instead. Finally the Poisson distribution is reflected.
