+++
title = "treemap"
+++

## treemap, tile type

The `treemap` tile displays a data table as a two-dimensional map, with one rectangle for each line, and the area of that rectangle proportional to that line's value.

The intent of `treemap` is to be an alternative to the `barchart` and `piechart` tiles with greater data density (since scaling is done based on rectangle area, rather than just bar width or arc size), but at the cost of labels or values on smaller rectangles not being visible.

```envision
table T = with
  [| as Total, as Name,     as Category,     as Color |]
  [| 7.0,    "USA",        "North America", "blue" |]
  [| 3.0,    "Canada",     "North America", "blue" |]
  [| 6.0,    "Germany",    "Europe",        "red"  |]
  [| 5.0,    "France",     "Europe",        "red"  |]
  [| 4.0,    "Italy",      "Europe",        "red"  |]
  [| 0.5,    "Luxembourg", "Europe",        "red"  |]

show treemap "By category (with color)" a1d4 with
  T.Total { value { color: #[T.Color] } }
  T.Name
  T.Category
```

The first series is the _value_, and should be a number strictly greater than zero 0. The second series is the _label_, and should be a text value. The third series is the _category_. The category is optional. When the category is present, it causes the contents of each category to be grouped in the display.

Hovering over any rectangle does display that rectangle's label and value, assuming that it is large enough to appear in the map at all.

Unlike `barchart` and `piechart`, there is a limit of 1000 elements that can be displayed in a `treemap` tile.

Unlike `barchart`, treemaps are also not able to display negative or zero values, and will report an error when they are encountered.

### Annex: complex example
<!-- Original dashboard at https://go.testing.lokad.com/d/21570/118010/victor-treemap -->
This annex illustrates the visuals that can be obtained with a treemap.

```envision-proto
show treemap "All" a1d6 F19143 with
  Items.TotalSales
  Items.Name
```

![Image](/images/treemap-all.png)

A _category_ is added.

```envision-proto
show treemap "By category" a1d6 F19143 with
  Items.TotalSales
  Items.Name
  Items.Category
```

![Image](/images/treemap-by-category.png)

A color gradient is chosen based on the tile color, with one color for each category.

```envision-proto
show treemap "All (with color)" a19d24 with
  Items.Total { value { color: #[Categories.Color[Items.Category]] } }
  Items.Name
```

![Image](/images/treemap-all-color.png)

The color can be independent of the category, but matching the color with category tends to produce a pleasing appearance:

```envision-proto
show treemap "By category (with color)" a13d18 with
  Items.Total { value { color: #[Categories.Color[Items.Category]] } }
  Items.Name
  Items.Category
```

![Image](/images/treemap-by-category-color.png)
