+++
title = "connected"
+++

## connected(T.a : text, T.b : text) 🡒 T.c : text, process

Considers the undirected graph described by all edges `(T.a,T.b)` and returns for each node `T.a` the name of the smallest node in `T.a`'s connected component. Here, _smallest_ means having the smallest name, in terms of text value comparison. The group is optional. When the group is specified, the table is first partitioned against the specified groups.

Example:

```envision
table T = with
  [| as Part, as CompatibleWith, as G |]
  [| "a", "b", 0 |]
  [| "b", "c", 0 |]
  [| "c", "a", 1 |]
  [| "d", "e", 1 |]

T.ComponentA = connected(T.Part, T.CompatibleWith)
T.ComponentB = connected(T.Part, T.CompatibleWith) by T.G

show table "" a1d4 with
  T.Part
  T.CompatibleWith
  T.CompatibleWith
  T.ComponentA
  T.ComponentB
```
