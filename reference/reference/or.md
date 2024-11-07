+++
title = "or"
+++

## (boolean or boolean) 🡒 boolean, const autodiff operator

The keyword `or` is the logical OR operator.

```envision
table T = with
  [| as A,  as B  |]
  [| false, false |]
  [| false, true  |]
  [| true,  false |]
  [| true,  true  |]

show table "" a1b4 with
  T.A
  T.B
  T.A or T.B
```

### See also

* [and](../../abc/and/).
* [not](../../mno/not/).
