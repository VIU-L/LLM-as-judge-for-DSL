+++
title = "scan"
+++

The keyword `scan` controls the ordering of the Envision processes.

## 'proc(expr1) scan expr2', ordering of the process

The `scan` option can be applied to any Envision process (the most common ones being the aggregators) to control the ordering of the operations over the processed table. The `auto` keyword can be placed after `scan` to follow the original ordering of the table.

```envision
table T = with
  [| as N, as L |]
  [| 1,    "b"  |]
  [| 0,    "a"  |]
  [| 2,    "c"  |]

def process myConcat(t: text) with
  keep txt = ""
  txt = "\{txt}\{t}"
  return txt

T.Asc = myConcat(T.L) scan T.N
T.Desc = myConcat(T.L) scan -T.N // inverse ordering
T.Aut = myConcat(T.L) scan auto // default table order

show table "" with T.N, T.L, T.Asc, T.Desc
// N,L,Asc,Desc,Aut
// 0,a,a,cba,b
// 1,b,ab,cb,ba
// 2,c,abc,c,bac
```
