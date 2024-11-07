+++
title = "hash"
+++

## hash(t: text) 🡒 number, pure function

Returns a pseudo-injective hash value between 0 and $2^{24}-1$.

Example:

```envision
table T = with
  [| as Word |]
  [| "The" |]
  [| "quick" |]
  [| "brown" |]
  [| "fox" |]
  [| "jumps" |]

show table "shuffled" a1b5 with
  hash(T.Word)
  T.Word
  order by hash(T.Word)
```

This function is typically used to randomly shuffle a dataset by hashing the content of a column, and then sorting against the hashed values.
