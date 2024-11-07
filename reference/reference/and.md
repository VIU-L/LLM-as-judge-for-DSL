+++
title = "and"
+++

The keyword `and` is the logical AND operator in Envision.

## (boolean and boolean) 🡒 boolean, const autodiff operator

When found in an expression, `and` is the logical AND operator.

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
  T.A and T.B
```

### See also

* [not](../../mno/not/).
* [or](../../mno/or/).
