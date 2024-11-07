+++
title = "match"
+++

## match, keyword

The keyword `match` offers a pattern matching mechanism. Range selectors are allowed for `date`, `number` and `text` types.

Example with `text` values:

```envision
table T = with
  [| as Code |]
  [| "a10"   |]
  [| "a11"   |]
  [| "a12"   |]
  [| "a13"   |]

T.Label = match T.Code with
  "a11" -> "Normal teardown"
  "a12" -> "Misuse"
  "a13" -> "Design defect"
  ..    -> "Unqualified scrap"

show table "Situations" a1c4 with
  T.Code
  T.Label
```

Example with `number` values:

```envision
table T = with
  [| as Value |]
  [| -7       |]
  [| 0        |]
  [| 1        |]
  [| 3        |]
  [| 99       |]

T.Label = match T.Value with
  0       -> "Zero"
  .. 0    -> "Negative"
  1       -> "One"
  2 .. 10 -> "A few"
  ..      -> "Many"

show table "Situations" a1c4 with
  T.Value
  T.Label
```
