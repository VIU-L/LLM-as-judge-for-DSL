+++
title = "fieldCount"
+++

## fieldCount(haystack: text, needle: text) 🡒 number, const pure function

Returns the same value as `countainscount(..) + 1`. This function is introduced to clarify a _parsing_ intent.

```envision
haystack = "a-b-c"
separator = "-"
n = fieldCount(haystack, separator)

table T = extend.range(n)
show table "Field Values" a1b3 with
    field(haystack, separator, T.N - 1) // displays a, b, c
```

## See also

* [field](../field/)
* [fieldr](../fieldr/)
