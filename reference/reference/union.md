+++
title = "union"
+++

## union(setA: long, setB: long) 🡒 long, pure function

Returns a [64-set](../../_/64set/) that is the union of the two provided sets, meaning the set of all elements that are provided in **either** input set.

```envision
AB = union(flag(1), flag(2))
BC = union(flag(2), flag(3))
show scalar "" a1c2 with union(AB, BC) // "{1,2,3}"
```

## union(set: long) 🡒 long, process function

Returns a [64-set](../../_/64set/) that is the intersection of all the provided sets. It is the process version of the `union(setA, setB)` pure binary function.

This is often used to aggregate a set of numbers in $\{0..63\}$ (especially month-days or week-days) into a set:

```envision
keep span date = date(2001,1,1) .. date(2001,12,31)

Month.DayCount = count(Day.*)
MonthDayCounts = union(flag(Month.DayCount))

// "{28,30,31}"
show scalar "" a1c2 with MonthDayCounts
```

If no `default` is specified, invoking this process over an empty range will return the empty set.
