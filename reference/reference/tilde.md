+++
title = "(~) uppercase operator"
+++

## (~ text) 🡒 text, const

The unary `~` operator returns the uppercase version of the text.

Example:

```envision
show summary "" a1b2 with
  ~"hello world!"
  contains(~"Hello World!", ~"heLLO")
```

This operator is an alias of the `uppercase` function.

### See also

* [uppercase](../../stu/uppercase/).
