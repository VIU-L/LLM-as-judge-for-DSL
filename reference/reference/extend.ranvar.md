+++
title = "extend.ranvar"
+++

## extend.ranvar(R : ranvar) 🡒 U.*, table function

Extends a ranvar into a table containing the inclusive segments of its buckets.

Example: 

```envision
x = poisson(3)
table G = extend.ranvar(x)
show table "poisson(3)" a1c5 with
  G.Min
  G.Max
  int(x, G.Min, G.Max) as "Probability"
```

The vectors `Min` and `Max` are present in the returned table which extends the table passed as argument. Those two values represent respectively the lower and higher inclusive boundaries of each segment. The segments are contiguous, and always include `[0, 0]`.

## extend.ranvar(R : ranvar, Gap : number) 🡒 U.*, table function

This overload of `extend.ranvar` (see above) ensures that both segments `[0, 0]` and `[1, gap]` are found in the resulting list of segments. Later segments are generated starting from `gap + 1`.

Example:

```envision
x = poisson(3)
gap = 4
table G = extend.ranvar(x, gap)
show table "poisson(3)" a1c5 with
  G.Min
  G.Max
  int(x, G.Min, G.Max) as "Probability"
```

This overload is typically intended to be used with the sum of the stock on hand plus the stock on order as the _gap_.

## extend.ranvar(R : ranvar, Gap : number, Multiplier : number) 🡒 U.*, table function

This overload of `extend.ranvar` (see above) ensures that

* both segments `[0, 0]` and `[1, gap]` are found in the resulting list of segments.
* later segments have a length equal to `multiplier` that is `[gap + 1, gap + multiplier]`, `[gap + multiplier + 1, gap + 2 * multiplier]`, etc.

Example:

```envision
x = poisson(3)
gap = 4
multiplier = 2
table G = extend.ranvar(x, gap, multiplier)
show table "poisson(3)" a1c5 with
  G.Min
  G.Max
  int(x, G.Min, G.Max) as "Probability"
```

This overload is typically intended to be used with _lot multiplier_ which are sometimes found among purchasing constraints.

## extend.ranvar(R : ranvar, Gap : number, Multiplier : number, Reach : number) 🡒 U.*, table function

This overload of `extend.ranvar` (see above) ensures that

* both segments `[0, 0]` and `[1, gap]` are found in the resulting list of segments.
* later segments have a length equal to `multiplier` that is `[gap + 1, gap + multiplier]`, `[gap + multiplier + 1, gap + 2 * multiplier]`, etc.
* the `Max` of last segment is greater or equal to the `reach`. Zero-probability segments are inserted as needed.

Example:

```envision
x = poisson(3)
gap = 4
multiplier = 5
reach = 20
table G = extend.ranvar(x, gap, multiplier, reach)
show table "poisson(3)" a1c5 with
  G.Min
  G.Max
  int(x, G.Min, G.Max) as "Probability"
```

This overload is typically intended to be used to cope with MOQs (Minimum Order Quantities). Indeed, as the MOQ may exceed the support of the ranvar, the segments may not go _far enough_ to reflect any eligible purchasing decision. This _reach_ overload mitigates this issue.

As a rule of thumb, we suggest not to use this overload unless there are specific MOQs to be reached. When this overload has to be used, it is suggested to keep `reach` as small as possible to limit the compute overhead. A small `reach` value does not prevent higher segments to be produced.

## See also

* [ranvar.buckets()](../../pqr/ranvar.buckets/)
