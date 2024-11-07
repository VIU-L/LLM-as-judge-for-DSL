+++
title = "assoc.quantity"
+++

## assoc.quantity(..) 🡒 number, process

Four arguments (in this order):

* `left: text`
* `leftQuantity: number`
* `right: text`
* `rightqty: number`

This process associates quantities from two sets connected by edges. Given two sets, left and right, represented by the `left` and `right` groups, the process takes the list of (left, right) edges connecting the two sets. Each set element has an associated initial quantity `same(leftQuantity) by left` or `same(rightQuantity) by right`. This quantity decreases over the course of the algorithm. Edges are visited in the specified order. The return value for the edge is set to the minimum of the two nodes' current quantity (the associated quantity), and that value is then subtracted from both quantities. In consequence, once a node's quantity reaches zero, it no longer contributes to the algorithm. If a `by` grouping is provided, each group is treated independently from all others.

<!-- TODO: example -->