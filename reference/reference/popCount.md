+++
title = "popCount"
+++

## popCount(set: long) 🡒 number, pure function

Given a [64-set](../../_/64set/), returns the total number of elements in that set, i.e. the cardinal, or _population count_, of that set.

Equivalently, returns the number of bits set to `1` in the binary representation of the provided 64-bit number.

```envision
ABC = union(flag(1), union(flag(2), flag(3)))
show scalar "" a1c2 with popCount(ABC) // 3
```

The value returned by `popCount` can be between 0 (for the empty set) and 64 (for the complement of the empty set).
