+++
title = "endsWith"
+++

## endsWith(source: text, pattern: text) 🡒 boolean, const pure function

Returns `true` if the source ends with an occurrence of the pattern.

```envision
source = "Hello World!"
show summary "" a1c2 with
  endsWith(source, "World") as "Ends with World"
  endsWith(source, "World!") as "Ends with World!"
```

## See also

* [startsWith](../../stu/startswith/)
