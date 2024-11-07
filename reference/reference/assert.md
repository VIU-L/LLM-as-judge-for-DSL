+++
title = "assert"
+++

## assert, tile type

This tile is intended to purposefully mark a run as _failed_ if certain conditions are not met with the data. A list of scalar boolean values can be listed after the `with` keyword.

```envision
a = 30
b = 50

show assert "My flags" with
  (a > 20) as "a is not greater than 20"
  (1 + b < 50) as "1+b is not lesser than 50" // FAIL!
```

The text value provided after the `as` keyword is passed to the error message.
