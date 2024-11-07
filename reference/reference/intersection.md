+++
title = "intersection"
+++

## intersection(setA: long, setB: long) 🡒 long, pure function

Returns a [64-set](../../_/64set/) that is the intersection of the two provided sets, meaning the set of all elements that are provided in **both** input set.

```envision
AB = union(flag(1), flag(2))
BC = union(flag(2), flag(3))
show scalar "" a1c2 with intersection(AB, BC) // "{2}"
```

## intersection(set: long) 🡒 long, process function

Returns a [64-set](../../_/64set/) that is the intersection of all the provided sets. It is the process version of the `intersection(setA, setB)` pure binary function.

```envision
table T = extend.range(63)
keep where T.N > 1

// The set of elements that are divided by each T.N
T.DividedBy = for N in T.N
  return union(flag(T.N)) 
         when (T.N > N and (T.N mod N) == 0)

Primes = intersection(complement(T.DividedBy))

// "{0,1,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61}"
show scalar "" a1c2 with Primes 
```

If no `default` is specified, invoking this process over an empty range will return `complement(emptySet())`, in other words the entire set $\{0\ldots 63\}$.
