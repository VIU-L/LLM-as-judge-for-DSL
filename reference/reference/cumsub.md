+++
title = "cumsub"
+++

## cumsub(..), process

<!-- TODO: [vermorel] 'cumsub' doc need to be rewritten. -->

The `cumsub()` function explores all bundles by increasing rank, keeping track of the remaining stock for each item.

It takes 4 vectors belonging to the same table `G` with:

* `G.Item`: the item identifier, all lines that share the same value belong to the same item;
* `G.Stock`: the initial stock for the item, all lines that belong to the same item must have the same `G.Stock` value;
* `G.Quantity`: the quantity of the item required for the purchase of the grid line;
* `G.Rank`: a _bundle_ identifier, all lines that share the same bundle identifier belong to the same bundle. It is forbidden to have two lines with the same `(G.Item, G.Rank)` pair. All bundles are ordered by increasing rank.

Initially, this stock is defined by the `G.Stock` vector. For each bundle, the function determines whether there is enough remaining stock to purchase _all_ grid lines in that bundle, based on whether the stock exceeds `G.Quantity`. If that is the case, then the function decrements the stock for each item, and writes to each grid line the remaining stock for that item. If there is not enough stock to serve the entire bundle - usually because one of the items has run out - then the function does not update the remaining stocks and stores for each grid line the value `-(S+1)` (where `S` is the remaining stock for that item at that point), to indicate both that the grid line is not purchased (test if `G.S < 0`) and whether it was that specific line that caused the bundle not to be purchased (test if `G.Quantity + G.S + 1 > 0`) and by how much (`G.Missing = G.Quantity + G.S + 1`).
