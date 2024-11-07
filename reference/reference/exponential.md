+++
title = "exponential"
+++

## exponential(lambda: number) 🡒 ranvar, pure function

Returns a probability distribution over $\mathbb{Z}$ obtained from the CDF of the exponential distribution with:

$$P_\lambda[X = n] =  F(n; \lambda) - F(n - 1; \lambda) $$

with

$$F(x;\lambda) = 1-e^{-\lambda x} \text{ if } x \ge 0 \text{ else } 0$$

The argument `lambda` must be positive or the function fails.

Example:

```envision
table T = with
  [| as N |]
  [|  0.5 |]
  [|  1.5 |]
  [|  2.5 |]

show table "" a1b4 with
  T.N
  exponential(T.N)
```

## See also

* The [exponential distribution](https://en.wikipedia.org/wiki/Exponential_distribution).
