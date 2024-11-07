+++
title = "sliceUrl"
+++

## sliceUrl(slice: ordinal) 🡒 text, pure function

Produces an [URL](../../stu/url/) that points to a specific slice of the dashboard produced by the run that executes this function. This URL can be used to offer a navigation UX that differs from the default slice selector.

```envision
table T[t] = with 
  [| as Product, as Color |]
  [| "Pant",     "Blue"   |]
  [| "Cap",      "Red"    |]
  [| "T-shirt",  "White"  |]

table Slices[slice] = slice by t title: T.Product

show table "One slice at a time" a1b2 slices: slice with
  T.Product
  T.Color

show table "Click to select a slice" a3b5 with
  T.Product { href: #[sliceUrl(T.slice)] }
```

Cannot be called on [try.lokad.com](https://try.lokad.com/).

To point to a slice of another dashboard, use [sliceSearchUrl](../../stu/slicesearchurl/) instead.

## sliceUrl(slice: ordinal, tab: text) 🡒 text, pure function

Produces an [URL](../../stu/url/) that points to a specific slice and tab of the dashboard produced by the run that executes this function.

```envision
table T[t] = with 
  [| as Product, as Color |]
  [| "Pant",     "Blue"   |]
  [| "Cap",      "Red"    |]
  [| "T-shirt",  "White"  |]

table Slices[slice] = slice by t title: T.Product

show table "One slice at a time (no color)" a1b2 slices: slice { tileTab: "noColor" } with
  T.Product

show table "One slice at a time (with color)" a1b2 slices: slice { tileTab: "Color" } with
  T.Product
  T.Color

show table "Click to select a slice" a3b5 with
  "\{T.Product} (no color)"  { href: #[sliceUrl(T.slice, "noColor")] }
  "\{T.Product} (with color)" { href: #[sliceUrl(T.slice, "Color")] }
```

Cannot be called on [try.lokad.com](https://try.lokad.com/).

To point to a slice of another dashboard, use [sliceSearchUrl](../../stu/slicesearchurl/) instead.
