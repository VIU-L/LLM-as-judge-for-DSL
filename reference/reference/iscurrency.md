+++
title = "iscurrency"
+++

## iscurrency(code: text) 🡒 boolean, pure function

Indicates whether the text value is a recognized currency code.

```envision
table T = with
  [| as Code |]
  [| "EUR" |]
  [| "USD" |]
  [| "AAA" |]

show table "" a1b3 with
  T.Code
  iscurrency(T.Code)
```

## See also

* [forex](../../def/forex/)
* [lastForex](../../def/lastforex/)
