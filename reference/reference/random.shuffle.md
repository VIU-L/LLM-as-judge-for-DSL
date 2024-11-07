+++
title = "random.shuffle"
+++

<!-- Beware 'random.shuffle' is not seeded at the moment:
https://lokad.atlassian.net/browse/LK-8540 -->

## random.shuffle(e: ordinal) 🡒 ordinal, general function

Returns a random permutation of the input vector.

```envision
table T[dim] = extend.range(6)

T.SuffledDim = random.shuffle(dim)
T.ShuffledN = T.N[T.SuffledDim] default fail

show table "" a1b7 with T.N, T.ShuffledN
```
