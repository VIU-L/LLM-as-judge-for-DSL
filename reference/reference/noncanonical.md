+++
title = "noncanonical"
+++

## noncanonical(T.a: text, T.b: text) 🡒 T.c : boolean, process

Returns `true` whenever a canonical representative for `T.a` cannot be computed. The pairs `(T.a, T.b)` are interpreted as graph edges with `T.a` as the source and `T.b` as the destination. The lack of representative happens when a circular path or a branching path gets detected.

Example:

```envision
table T = with
  [| as OldCode, as Replacement |]
  [| "x-00",  "ax-00" |]
  [| "x-01",  "ax-01" |]
  [| "x-02",  "ax-02" |]
  [| "ax-00", "x-00" |]

T.HasNoRepresentative = noncanonical(T.OldCode, T.Replacement)

show table "" a1c4 with
  T.OldCode
  T.Replacement
  T.HasNoRepresentative
```

From a practical perspective, this process is intended to deal with code replacement (ex: SKU code replacement) as illustrated in the above example.

### See also

* [canonical](../../abc/canonical/).
