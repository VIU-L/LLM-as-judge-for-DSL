+++
title = "flagset"
+++

## flagset, data type

The `flagset` data type is supported by Envision:

```envision
a = flag(1) // {1}
b = union(a, flag(2)) // {1,2}
c = intersection(b, flag(2)) // {2}
show summary "" with a, b, c
```

Under the hood, the `flagset` is implemented as `uint64` values.

The keyword `flagset` appears in user-defined functions:

```envision
def pure set42(f : flagset) with
  return union(f, flag(42))

show scalar "" with set42(flag(13)) // {13, 42}
```

and in `read` blocks:

```envision
read "/sample.csv" as Sample with
  MyFlagset : flagset
```
