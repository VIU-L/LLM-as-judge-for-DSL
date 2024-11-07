+++
title = "padLeft"
+++

## padLeft(source: text, pad: text, size: number) 🡒 text, const pure function

Prepends `pad` - _in its entirety_ - to `source` until the resulting text value's length is _equal to_ or _greater than_ the target `size`. If `size` is lower than `source`'s length, padding is not applied.

```envision
show summary "" a1c3 with
  padLeft("1234","0", 7) // returns "0001234"
  padLeft("1234","0_", 7) // returns "0_0_1234"
  padLeft("1234","0__", 7) // returns "0__1234"
  padLeft("1234","0__", 3) // returns "1234"
```

The following restrictions apply, otherwise the function fails:

* `pad` must be non-empty.
* `size` must be an integer in the segment \[1, 256\].
