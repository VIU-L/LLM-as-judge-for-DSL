+++
title = "not"
+++

## (not boolean) 🡒 boolean, const autodiff operator

The keyword `not` is the logical NOT operator.

```envision
table T = with
  [| as A  |]
  [| false |]
  [| true  |]

show table "" a1b2 with
  T.A
  not T.A
```

### See also

* [and](../../abc/and/).
* [or](../../mno/or/).
