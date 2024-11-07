+++
title = "sliceSearchUrl"
+++

## sliceSearchUrl(script: number, pattern: text, tab: text) 🡒 text, pure function

Returns the [URL](../../stu/url/), encoded as a text value, that points to a specific slice within the latest dashboard produced by a script.

The dashboard is identified by its script identifier passed as the first argument `script`.

The slice is identified by the second argument `pattern`, which acts as a query performed on the dashboard. If there are multiple matching slices, the first slice (name-wise) is selected.

If a tab exists that matches the third agument `tab`, then that tab is opened.

Example:

```envision
projectId = 12345 // found in the URL of the project

table Queries = with
  [| as Q |]
  [| "pant" |]
  [|  "hat" |]
  [|  "cap" |]

Queries.Url = sliceSearchUrl(projectId, Queries.Q)

show table "" a1c3 with
  Queries.Q { href: #[Queries.Url] }
```

Cannot be called on [try.lokad.com](https://try.lokad.com/).

## sliceSearchUrl(script: number, pattern: text) 🡒 text, pure function

Like `sliceSearch(script, pattern, tab)` above, but points to the first tab of the dashboard.

Cannot be called on [try.lokad.com](https://try.lokad.com/).

## sliceSearchUrl(pattern: text) 🡒 text, pure function

Like `sliceSearch(script, pattern, tab)` above, but points to the first tab of the latest dashboard produced by the currently executing script.

This function cannot be called from [modules](/language/modules/), from [user-defined functions](/language/functions/), or on [try.lokad.com](https://try.lokad.com/).

## sliceSearchUrl(pattern: text, tab: text) 🡒 text, pure function

Like `sliceSearch(script, pattern)` above, but points to the latest dashboard produced by the currently executing script.

This function cannot be called from [modules](/language/modules/), from [user-defined functions](/language/functions/), or on [try.lokad.com](https://try.lokad.com/).
