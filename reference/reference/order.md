+++
title = "order"
+++

## order by, keyword, tile option

The `order by` is a tile option that can be added after the columns provided to the tile:

```envision
table T = with
  [| as Id, as X |]
  [| "a", 3 |]
  [| "b", 1 |]
  [| "c", 4 |]

show table "" with  // displays b, a, c
  T.Id
  order by T.X // 'order by'  is after the columns of the tile
```

Alternatively, `desc` can be used to invert the ordering:

```envision
table T = with
  [| as Id, as X |]
  [| "a", 3 |]
  [| "b", 1 |]
  [| "c", 4 |]

show table "" with  // displays c, a, b
  T.Id
  order by T.X desc
```
