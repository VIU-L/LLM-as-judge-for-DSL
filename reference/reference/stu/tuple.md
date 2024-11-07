+++
title = "tuple"
+++

## tuple, language construct

Envision supports scalar tuples:

```envision
myTuple = (1, "y") // parenthesis are mandatory to define a tuple
a, b = myTuple // deconstruct the scalar tuple
show summary "" with a, b // 1, y
```

Vector tuples are also supported:

```envision
table T = extend.range(5) // 'T.N' implicitely created, 5 lines

T.myTuple = each T // enumerate the table 'T'
  // 2-space indent, we are within the 'each' block
  a = T.N + 1 // 'T.N' is scalar, due to 'each' block
  b = T.N * 2 // 'a' and 'b' are scalar too
  return (a, b) // return a tuple

T.A, T.B = T.myTuple // deconstruct the vector tuple

show table "" with T.A, T.B // 5 lines
```

User-defined functions can return tuples:

```envision
def pure myFun(x : number) with
  // 2-space indent, we are within the 'def' block
  return (x, x + 1) // returns a tuple, beware parenthesis are necessary

myTuple = myFun(42)
a, b = myTuple

show summary "" with a, b // 42, 43
```

At this point, user-defined functions do not support tuple parameters. Thus, tuples have to be deconstructed first, before passing the individual component of the tuple to the user-defined function.
