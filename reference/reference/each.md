+++
title = "each"
+++

## each, keyword

The `each` keyword offers an iteration mechanism against an observation table. Iterations are not ordered.

```envision
table Obs = with
  [| as N |]
  [| 1 |]
  [| 2 |]
  [| 3 |]

Obs.Cpy = each Obs
  cpy = Obs.N + 1
  return cpy

show table "" a1b3 with Obs.N, Obs.Cpy
```

## each .. scan , keyword

The `each .. scan` keywords offer an iteration mechanism against an observation table. Iterations are ordered based on the argument passed to `scan`.

```envision
table Obs = with
  [| date(2021, 1, 1) as Date, 13 as Quantity |]
  [| date(2021, 2, 1)       ,  11             |]
  [| date(2021, 3, 1)       ,  17             |]
  [| date(2021, 4, 1)       ,  18             |]
  [| date(2021, 5, 1)       ,  16             |]

Best = 0

Obs.BestSoFar = each Obs scan Obs.Date
  keep Best
  NewBest = max(Best, Obs.Quantity)
  Best = NewBest
  return NewBest

show table "" a1b4 with Obs.Date, Obs.BestSoFar
```
