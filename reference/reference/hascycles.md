+++
title = "hasCycles"
+++

## hasCycles(T.a: text, T.b: text) 🡒 T.c : boolean, process

The functions interprets the pairs `(T.a, T.b)` as the edges of a directed graph and returns `true` for every edge that is part of a cycle.

```envision
table Edges = with 
  [| as A, as B |]  // HasCycles
  [| "1", "2" |]    // false
  [| "2", "3" |]    // true
  [| "3", "4" |]    // true
  [| "4", "2" |]    // true
  [| "5", "5" |]    // true
  [| "5", "6" |]    // false

Edges.HasCycles = hasCycles(Edges.A, Edges.B)

show table "Part of cycles" a1b6 with
  Edges.A
  Edges.B
  Edges.HasCycles
```

## See also

* [extend.billOfMaterials](../../def/extend.billofmaterials/)
