+++
title = "def"
+++

The keyword `def` is used in Envision to introduce user-defined functions.

## 'def funtype funname (args) with', function definition

User-defined functions can be introduced with `def`:

```envision
def pure helloWorld() with
  return "Hello World!"

def pure myMax(x : number, y : number) with
  if x > y
    return x
  else
    return x + y

def pure swap(a : text, b : text) with
  return (b, a) // wrapping '(..)' needed, indicates a tuple

show scalar "" with helloWorld() // Hello World!
show scalar "" with myMax(2, 17) // 17

a, b = swap("foo", "bar")
show summary "" with a /* bar */, b /* foo */
```

The return type is implicit, based on the returned values. Envision does not support expliciting the return type of user-defined function.

## See also

* [pure (function modifier)](../../pqr/pure/)
* [process (function modifer)](../../pqr/process/)
* [User defined functions](../../language/functions/)
