+++
title = "fieldr"
+++

## fieldr(haystack: text, separator: text, index: number) 🡒 text, const pure function

Returns the n<sup>th</sup> field, zero-indexed **from the right**, in a text value that contains multiple sub-text value separated by a specified separator.

```envision
haystack = "a-b-c-d-"
show summary "" a1c3 with
  fieldr(haystack, "-", 0) // returns ""
  fieldr(haystack, "-", 1) // returns "d"
  fieldr(haystack, "-", 2) // returns "c"
```

This function is intended to facilitate parsing values that have been concatenated within a single table column.

## See also

* [field](../field/)
* [fieldCount](../fieldcount/)
