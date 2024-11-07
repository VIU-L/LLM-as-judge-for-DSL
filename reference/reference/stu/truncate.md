+++
title = "truncate"
+++

## truncate(r: ranvar, a: number, b: number) 🡒 ranvar, pure function

Returns the conditional ranvar between the inclusive boundaries \[`a`, `b`\]. This function is almost equivalent to `min(max(r, a), b)`, except that it fails if the first argument is greater than the second.

```envision
show scalar "poisson(3)" a1c3 with poisson(3)
show scalar "truncate(poisson(3), 2, 5)" a4c6 with truncate(poisson(3), 2, 5)
```
