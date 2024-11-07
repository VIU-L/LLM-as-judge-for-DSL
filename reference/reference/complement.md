+++
title = "complement"
+++

## complement(set: long) 🡒 long, pure function

Returns the complement of a [64-set](../../_/64set/), that is, the set of all elements $\{0\ldots 63\}$ that are not in the original set.

```envision
table T = extend.range(64)
OddNumbers = union(flag(T.N)) when (T.N mod 2 == 1)
EvenNumbers = complement(OddNumbers)
show summary "" a1c2 with
  OddNumbers as "Odd Numbers"   // {1,3,..,63}
  EvenNumbers as "Even Numbers" // {0,2,..,62}
```
