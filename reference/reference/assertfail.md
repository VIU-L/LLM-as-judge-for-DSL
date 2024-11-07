+++
title = "assertfail"
+++

## assertfail(err : text) 🡒 unit, pure function

The function creates an error which interrupts the execution of a script. The function is only intended to be called within the declaration block of a user-defined function. The text value passed as argument is used as the error message.

```envision
def pure myCubeRoot(x : number) with
  if x < 0
    _ = assertfail("Value should be non-negative but was: \{x}")
  return x^(1/3)

show scalar "" with myCubeRoot(-1) // fails!
```

The return value of `assertfail` is not significant, thus it is advised to always use the discard (`_`) for the assignment.
