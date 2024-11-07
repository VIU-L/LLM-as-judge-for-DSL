+++
title = "substr"
+++

## substr(source: text, start: number) 🡒 text, const pure function

Defined as `substr(text, number, +infinity)`, see below.

```envision
source = "Hello World!"
show summary "" a1a4 with
  substr(source, 0)  // returns "Hello World!"
  substr(source, -3) // returns "ld!"
  substr(source, 6) // returns "World!"
  substr(source, 100) // returns ""
```

## substr(source: text, start: number, count: number) 🡒 text, const pure function

Return a sub-value from the text.

When nonnegative, `start` is the offset from the beginning of the text value, otherwise it's an offset from the end of the text value.

The length of the returned text value is defined by `count`, which gets treated as zero when negative.

If the targeted segment of characters is partially or completly outside the text value, then the segment is clipped to fit.

```envision
source = "Hello World!"
show summary "" a1a4 with
  substr(source, 0, 3) // returns "Hel"
  substr(source, -3, 2) // returns "ld"
  substr(source, 6, 100) // returns "World!"
  substr(source, 100, 100) // returns ""
```
