+++
title = "trim"
+++

## trim(t: text, toTrim: text) 🡒 text, const pure function

The function returns a shortened version of the text value passed as the first argument. The second argument is the list of characters to be removed from both start and end, i.e. the list of characters to be trimmed.

```envision
const original = " Hello world! "
const trimmed1 = trim(original, " ")
const trimmed2 = trim(original, "! ")
show summary "Trim" a1c1 with 
  strlen(original) as "\{original}"
  strlen(trimmed1) as "\{trimmed1}"
  strlen(trimmed2) as "\{trimmed2}"
```
