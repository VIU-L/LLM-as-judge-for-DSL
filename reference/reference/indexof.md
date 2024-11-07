+++
title = "indexOf"
+++

## indexOf(source: text, pattern: text) 🡒 number, const pure function

Returns the index of the first occurrence of the pattern within the text, or −1, if no such occurrence is found.

```envision
source = "Hello World!"
show summary "" a1c3 with
  indexOf(source, "o")
  indexOf(source, "!")
  indexOf(source, "Z")
```

The index value returned by `indexOf` is frequently intended to be later consumed by the function `substr`.

## See also

* [substr](../../stu/substr/)
