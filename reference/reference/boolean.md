+++
title = "boolean"
+++

## boolean, data type

The `boolean` data type is supported by Envision:

```envision
a = true
b = not a // false
c = a and b // false
d = a or b // true
show summary "" with a, b, c, d
```

The keyword `boolean` appears in user-defined functions:

```envision
def pure myXor(a : boolean, b : boolean) with
  return (a and not b) or (not a and b)

show scalar "" with myXor(true, false) // true
```

and in `read` blocks:

```envision
read "/sample.csv" as Sample with
  MyBoolean : boolean
```
