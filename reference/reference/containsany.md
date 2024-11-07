+++
title = "containsAny"
+++

## containany(haystack: text, needles: text, separator: text) 🡒 boolean, pure function

Indicate whether the haystack contains any needle, as obtained by splitting the second argument through the third argument.

```envision
haystack = "1+2+3+4"
needles = "-,+,*,/"
separator = ","

show scalar "" with 
    containsAny(haystack, needles, separator) // 'true'
```

The separator, i.e. the third argument, is not allowed to be empty.
