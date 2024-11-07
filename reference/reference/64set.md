+++
title = "64-Sets"
+++

## 64-set, language concept

Some functions treat values of the `long` type as 64 separate bits, representing a subset of $\{0\ldots 63\}$. This acts as a high-performance representation of a set of integers, in cases where using relational logic is not fast enough.

64-sets are created with [flag](../../def/flag/) or [emptySet](../../def/emptyset/).

They can be combined with [union](../../stu/union/) and [intersection](../../ghi/intersection/), negated with [complement](../../abc/complement/), and compared with [isSubsetOf](../../ghi/issubsetof/) or [contains](../../abc/contains/).

`A == B` and `A != B` work as expected to check if two sets are exactly equal or not.

The number of elements in a 64-set is given with [popCount](../../pqr/popcount/).

```envision
AB = union(flag(1), flag(2))
BC = union(flag(2), flag(3))
ABC = union(flag(1), union(flag(2), flag(3)))

show summary "" with
  union(AB, BC) // "{1,2,3}"
  intersection(AB, BC) // "{2}"
  popCount(ABC) // 3
  isSubsetOf(BC, ABC) // true
```

### Motivation

While typical Envision use-cases involve utilizing tables and vectors for representing sets, these methods can become performance bottlenecks or may be incompatible with certain operations like nested `cross` functions. 64-sets offer a streamlined, performance-optimized approach to handle boolean representations for a range of scenarios including iterative functions (`for`, `each`), Monte Carlo simulations, and more.

64-sets are particularly useful when dealing with temporal sets (weekdays, weeks of the year, months over several years), part bundles, or categories where the overhead of cross-tables could become prohibitive or even infeasible.

While 64-sets offer computational efficiency, they are restricted to representing integers in the range of $\{0\ldots 63\}$. Therefore, they may not be suitable for all scenarios.

By integrating 64-sets into your Envision workflow, you trade some ease-of-use for computational speed, thereby making them a specialized tool for performance-critical applications.
