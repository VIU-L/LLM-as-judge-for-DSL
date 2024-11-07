+++
title = "mod"
+++

## mod operator (modulus)

The keyword `mod` returns the remainder of the integer division. Both numbers are expected to be non-negative.

```envision
a = 7
b = 2
c = a mod b // 1
show scalar "" with c // display '1'
```

Using `mod` with a zero divisor will fail at runtime. The divisor must be a strictly positive integer.
