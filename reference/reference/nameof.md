+++
title = "nameof"
+++

## nameof(expr) 🡒 text, const

A `nameof` expression returns a text value representing the expression passed as argument, such as `nameof(1 + 2)` returning `"1 + 2"`. The argument is _not_ evaluated !

As a special case, `nameof(T.X)` returns `X` instead of `T.X`, and `nameof("XYZ")` returns `"XYZ"` instead of `"\"XYZ\""`.

The following example

```envision
table Example = with
  [| as Index, as Country, as CapitalCity |]
  [| 1,        "France",   "Paris"        |]
  [| 2,        "Greece",   "Athens"       |]
  [| 3,        "Hungary",  "Budapest"     |]
  [| 4,        "Italy",    "Rome"         |]

chosen = 2
where Example.Index == chosen
  capitalH = nameof(Example.CapitalCity)
  country = single(Example.Country)
  capital = single(Example.CapitalCity)
  show scalar "" a1c1 with "\{capital} is the \{capitalH} of \{country}."
```

will display `Athens is the CapitalCity of Greece.`.
