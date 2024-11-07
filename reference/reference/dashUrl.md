+++
title = "dashUrl"
+++

## dashUrl(script: number) -> text, pure function

Produces an [URL](../../stu/url/) which, when visited, redirects to the latest dashboard of the script with the identifier `script`.

```envision
show menu "Navigation" with 
  "Next Step" { href: #(dashUrl(10000)) }
  "Previous Step" { href: #(dashUrl(20000)) }
```

This function cannot be called on [try.lokad.com](https://try.lokad.com/).

To point to a specific slice of that dashboard, use [sliceSearchUrl](../../stu/slicesearchurl/) instead.

## dashUrl(script: number, tabSearch: text) -> text, pure function

Produces an [URL](../../stu/url/) which, when visited, redirects to the latest dashboard of the script with the identifier `script`, and opens the [tab](../../stu/tabs/) named `tabSearch`.

This function cannot be called on [try.lokad.com](https://try.lokad.com/).

To point to a specific slice of that dashboard, use [sliceSearchUrl](../../stu/slicesearchurl/) instead.

## dashUrl() -> text, pure function

Produces an [URL](../../stu/url/) which, when visited, redirects to the latest dashboard of the script from which it was called.

This function cannot be called from [modules](/language/modules/), from [user-defined functions](/language/functions/), or on [try.lokad.com](https://try.lokad.com/).

To point to the dashboard produced by the run that calls the function (even when it is no longer the latest dashboard of its script), use [currentDashUrl](../../abc/currentdashurl/) instead.

To point to a specific slice of that dashboard, use [sliceSearchUrl](../../stu/slicesearchurl/) instead.

## dashUrl(tabSearch: text) -> text, pure function

Produces an [URL](../../stu/url/) which, when visited, redirects to the latest dashboard of the script or instance from which it was called, and opens the [tab](../../stu/tabs/) named `tabSearch`.

This function cannot be called from [modules](/language/modules/) or from a [user-defined functions](/language/functions/), or on [try.lokad.com](https://try.lokad.com/).

To point to a specific slice of that dashboard, use [sliceSearchUrl](../../stu/slicesearchurl/) instead.
