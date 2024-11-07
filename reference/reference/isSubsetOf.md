+++
title = "isSubsetOf"
+++

## isSubsetOf(setA: long, setB: long) 🡒 long, pure function

Given two [64-sets](../../_/64set/), returns `true` if $A \subset B$ (A is a non-strict subset of B).

```envision
ABC = union(flag(1), union(flag(2), flag(3)))
BC  = union(flag(2), flag(3))
show scalar "" a1c2 with isSubsetOf(BC, ABC) // true
```
