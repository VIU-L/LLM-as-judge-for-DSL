+++
title = "argmax"
+++

## argmax(T.a : number, T.b : 'b)  🡒 'b, autodiff aggregator

Returns the paired value associated with the highest number. The aggregator takes two arguments. The first argument is the number used for the ordering. The second argument is the paired valued, one of them being returned.

```envision
table T = with
  [| as A, as B |]
  [| 2,   "c"   |]
  [| 0,   "a"   |]
  [| 1,   "b"   |]

V = argmax(T.A, T.B)

show scalar "T.B value at highest T.A" with V
```

### See also

* [argmin](../argmin/).
