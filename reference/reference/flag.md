+++
title = "flag"
+++

## flag(n: number) 🡒 long, pure function

Returns a [64-set](../../_/64set/) that contains only the provided integer `n`.

```envision
show scalar "" a1c2 with flag(42) // "{42}"
```

It is an error to provide a fractional number, or a number smaller than 0 or greater than 63.

This function is often used in conjunction with [union](../../stu/union/) to construct larger 64-sets.
