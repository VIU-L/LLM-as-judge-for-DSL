+++
title = "zoz"
+++

## zoz(z: zedfunc) 🡒 zedfunc, pure function

Returns _zero on zero_, an identical zedfunc except that the value is set to zero on zero.

```envision
a = max(constant(10) - linear(1) * linear(1), 0)
show scalar "a" a1c3 with a
show scalar "zoz(a)" a4c6 with zoz(a)
```
