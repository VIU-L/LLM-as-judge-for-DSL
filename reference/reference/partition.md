+++
title = "partition"
+++

## partition(max: number) 🡒 number, process

The `partition` is a utility process intended to facilitate the parallelization of large processing tasks via the `loop` block.

```envision
table T[t] = extend.range(100)
T.X = 0 // dummy initialization

T.Part = partition(10) scan t
i = -1
loop 10
  i = i + 1
  keep where T.Part == i
  T.X = T.N^2 // here, the expensive calculation

show table "Squares" a1a4 with T.X
```

### Annex: implementation

The `partition` process could be manually re-implemented as:

```envision
def process partition_bis(max: number) default 1 with 
  keep prev = 0
  prev = if prev >= max then 1 else prev + 1
  return prev
```
