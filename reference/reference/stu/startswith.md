+++
title = "startsWith"
+++

## startsWith(source: text, pattern: text) 🡒 boolean, const pure function

Returns `true` if the source starts with an occurrence of the pattern.

```envision
source = "Hello World!"
show summary "" a1c2 with
  startsWith(source, "hello") as "Starts with hello"
  startsWith(source, "Hello") as "Starts with Hello"
```

## See also

* [endsWith](../../def/endswith/)
