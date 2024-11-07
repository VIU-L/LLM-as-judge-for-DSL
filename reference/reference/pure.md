+++
title = "pure"
+++

The contextual keyword `pure` specifies the type of a user-defined function.

## 'def pure funname (params) with', simple mapping definition

The modifier `pure` indicates that the function is a simple mapping taking scalar arguments.

```envision
def pure diskSurface(r : number) with
  return 3.1416 * r * r

show scalar "" with diskSurface(2) // ~12.57
```

A pure function has no side-effect. Its arguments cannot be assigned.

## See also

* [def](../../def/def/)
* [process](../../pqr/process/)
* [User defined functions](../../../language/functions/)
