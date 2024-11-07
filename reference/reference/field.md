+++
title = "field"
+++

## field(haystack: text, separator: text, index: number) 🡒 text, const pure function

Returns the n<sup>th</sup> field, zero-indexed **from the left**, in a text value that contains multiple sub-text values separated by a specified separator.

```envision
haystack = "a-b-c-d-"
show summary "" a1c3 with
  field(haystack, "-", 0) // 'a'
  field(haystack, "-", 1) // 'b'
  field(haystack, "-", 2) // 'c'
```

This function is intended to facilitate parsing values that have been concatenated within a single table column.

## See also

* [fieldCount](../fieldcount/)
* [fieldr](../fieldr/)
