+++
title = "priopack"
+++

<!-- TODO: 'priopack' needs rewrite -->

## priopack(V, MaxV, JT, B) by [Group] sort [Order], function

A simple variant of the [bin packing algorithm](https://en.wikipedia.org/wiki/Bin_packing_problem) intended to be used with a purchase prioritization list. Unlike the classic bin packing algorithm, not only do we seek to optimize the bin capacities, but the ordering of the units will also be preserved as much as possible.

* `V` is the volume of each line.
* `MaxV` is the max volume capacity, its value is homogeneous to `V`, and it is assumed to be a constant value across the equivalent class `Group`.
* `JT` is the jumping threshold, its value is homogeneous to `V`, it is typically expected to be a small multiple of the `Group` value.
* `B` is an optional argument interpreted as the _barrier_, when this value is provided, the bin-packing process is not allowed to reorder lines that belong to the same equivalence class as defined by `B`.
* `Group` is the equivalence class of the suppliers, with bin packing computed _per supplier_.
* `Order` contains the ranks of the lines to be packed.
