+++
title = "containsCount"
+++

## containsCount(haystack: text, needle: text) 🡒 number, const pure function

Returns the number of occurrences of the second argument within the first argument.

```envision
haystack = "Hello World!"
show summary "" a1c2 with
  containsCount(haystack, "l") as "Contains 'l'?"         // '3'
  containsCount(haystack, "World") as "Contains 'World'?" // '1'
```

The second argument is not allowed to be an empty text value.
