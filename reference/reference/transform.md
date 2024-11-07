+++
title = "transform"
+++

## transform(r: ranvar, a: number) 🡒 ranvar, pure function

Let $X$ be the random variable over $\mathbb{Z}$ associated to the ranvar `r`. This function returns the ranvar associated with the random variable $\mathrm{round}(aX)$.

Example:

```envision
show scalar "poisson(2)" a1c3 with poisson(2)
show scalar "transform(poisson(2), 3)" a4c6 with transform(poisson(2), 3)
```
