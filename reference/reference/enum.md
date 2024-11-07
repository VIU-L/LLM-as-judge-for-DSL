+++
title = "enum"
+++

## enum (extension), keyword

The `enum` keyword is used to introduce a complex data type from an enumeration of its values.

```envision
table enum Countries = "BE", "FR", "UK", "US"

show table "Countries" a1b4 with
  text(Countries.Value)
  "(\{Countries.Label})"
 
be = enum<<Countries>>("BE")
show scalar "Belgium" c1 with text(be)
```

## enum (comprehension), function

The `enum` keyword is used to introduce a complex data type from a vector that contains its values.

```envision
table T = with 
  [| as Country|]
  [| "BE" |]
  [| "FR" |]
  [| "UK" |]
  [| "US" |]

table enum Countries = T.Country
 
show table "Countries" a1b4 with
  text(Countries.Value)
  "(\{Countries.Label})"
 
be = enum<<Countries>>("BE")
show scalar "Belgium" c1 with text(be)
```
