+++
title = "spark"
+++

## spark(r: ranvar) 🡒 text, pure function

 Returns a text value that contains compact ascii-art representation of the ranvar.

Example:

```envision
table T = with
  [| as Lambda |]
  [|  1 |]
  [|  2 |]
  [|  5 |]
  [|  10 |]

show table "" a1b4 with
  T.Lambda
  spark(poisson(T.Lambda))
```
