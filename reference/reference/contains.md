+++
title = "contains"
+++

## contains(haystack: text, needle: text) 🡒 boolean, const pure function

Returns `true` if the first argument contains an occurrence of the second argument.

```envision
haystack = "Hello World!"
show summary "" a1c2 with
  contains(haystack, "Hello") as "Contains Hello?" // 'true'
  contains(haystack, "Town") as "Contains Town?"   // 'false'
```

The second argument is not allowed to be an empty text value.

## contains(haystack: long, needle: number) -> boolean, pure function

Given `haystack` a [64-set](../../_/64set/) and `needle` a number, returns true if the needle is an element of the haystack, and false otherwise.

```envision
haystack = union(flag(10), flag(20))
show summary "" a1c2 with 
  contains(haystack, 10) as "Contains 10?" // 'true'
  contains(haystack, 15) as "Contains 15?" // 'false'
```

It is an error to provide a `needle` that is not an integer, smaller than 0 or greater than 63.
