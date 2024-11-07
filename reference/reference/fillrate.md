+++
title = "fillrate"
+++

## fillrate(r: ranvar) 🡒 ranvar, pure function

Returns the marginal contribution to the fill rate by stock position.

Example:

```envision
r = poisson(3)
show scalar "poisson(3)" a1c3 with r
show scalar "fillrate(poisson(3))" a4c6 with fillrate(r)
```

## See also

* [Fill rate definition](https://www.lokad.com/fill-rate-definition)
