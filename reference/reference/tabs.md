+++
title = "tabs"
+++

## tabs, tile type

The `tabs` tile defines two or more _tabs_ on the dashboard, so that every other tile can be associated with one of the tabs (or remain independent of the tabs). The tile is displayed as a tab selector to show which tab is currently being displayed, and to allow selecting another:

![Image](/images/show-tabs.png)

The above image is produced by:

```envision
show tabs "" a1b1 with
  "Demand"
  "Leadtime"
```

This creates two tabs named `"Demand"` and `"Leadtime"`.  

To associate a tile with a tab, use the [tileTab](../../../specifications/stylecode/properties/tileTab) StyleCode property, using the name of the tab as the value:

```envision
// Only appears on the "Demand" tab
show label "Product Demand" a2b2 { tileTab: "Demand" }

// Only appears on the "Leadtime" tab
show label "Purchase Lead Time" a2b2 { tileTab: "Leadtime" }
```

Note that it is possible for two tiles to share the same position (here, `a2b2`) so long as they are on different tabs.

If `tileTab: default` is specified (or there is no `tileTab`), the tile appears on all tabs.

The `tabs` tile is not supported yet in the playground.
