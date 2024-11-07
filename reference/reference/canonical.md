+++
title = "canonical"
+++

## canonical(T.a: text, T.b: text) 🡒 T.c : text, process

Returns the canonical representative for each `T.a` value. The pairs `(T.a, T.b)` are interpreted as graph edges with `T.a` as the source and `T.b` as the destination.

Example:

```envision
table T = with
  [| as OldCode, as Replacement |]
  [| "x-00",  "ax-00" |]
  [| "x-01",  "ax-01" |]
  [| "x-02",  "ax-02" |]
  [| "ax-00", "ax-03" |]

T.NewCode = canonical(T.OldCode, T.Replacement)

show table "" a1c4 with
  T.OldCode
  T.Replacement
  T.NewCode
```

From a practical perspective, this process is intended to deal with code replacement (ex: SKU code replacement) as illustrated in the above example.

### See also

* [noncanonical](../../mno/noncanonical/).
