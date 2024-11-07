+++
title = "uniform"
+++

## uniform(a : number) 🡒 zedfunc, pure function

Returns the constant function $f: x \mapsto 1$ on the segment $[0, a]$ and zero otherwise. The argument `a` must be an integer or the function fails.

Example:

```envision
show scalar "" a1b2 with uniform(5)
```

## uniform(a : number, b : number) 🡒 zedfunc, pure function

<!-- 'uniform(a,b)' too tolerant to invalid input 
https://lokad.atlassian.net/browse/LK-6788 -->

Returns the constant function $f: x \mapsto 1$ on the segment $[a, b]$ and zero otherwise. The arguments `a` and `b` must be integers or the function fails. Also, $a \leq b$ other the function fails.

Example:

```envision
show scalar "" a1b2 with uniform(3, 6)
```
