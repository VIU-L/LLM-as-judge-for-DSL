+++
title = "dispersion"
+++

## dispersion(r: ranvar) 🡒 number, pure function

Returns the dispersion of the specified ranvar. The dispersion is defined as the variance divided by the mean. It is defined only if the mean is strictly greater than zero.

```envision
r = negativeBinomial(/* mean */ 2, /* dispersion */ 1.5)
show scalar "" with dispersion(r) // 1.50
```
