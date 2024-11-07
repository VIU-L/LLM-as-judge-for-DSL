+++
title = "mkuid"
+++

## mkuid(T.a : 'a) 🡒 number, special function

Same as `mkuid(T.a, "")`, see below.

## mkuid(T.a : 'a, offset: number) 🡒 number, special function

Returns a unique number, with unicity maintained across Envision runs. This function is intended to uniquely identify results calculated by Lokad. For example, it can be used to generate a unique _purchase order number_ to be incremented whenever the Envision script is re-executed.

The vector `T.a` is ignored, but the UID (unique identifier) is generated as a scalar in the table `T`.

The `offset` is a scalar that represents the starting suffix for the UID. The generated text values are numbers in the format `PPPPPPPAAA`, with `P` as a page number (does not start with 0) that is always strictly increasing, and `A` as an incremented counter that starts at offset (or 0 if no offset parameter is provided). `P` has at least 7 digits, `A` has at least 3.

The UIDs offer three properties.

1. All UIDs can be parsed as numbers, and those numbers will be different. Keep in mind, however, that UIDs have at least 10 digits, and likely more if each call needs to generate more than 1000.
2. A UID generated at time T is strictly inferior (in alphabetical order) to a UID generated at time T' > T.
3. If all calls generate similar numbers of UIDs (less than 999, or between 1000 and 9999, etc.) then the previous property is also true for the numeric order between UIDs.

Example:

```envision
table T = with
  [| as Word |]
  [| "The" |]
  [| "quick" |]
  [| "brown" |]
  [| "fox" |]
  [| "jumps" |]

show table "unique identier" a1b5 with
  mkuid(T.Word, 123)
  T.Word
```
