+++
title = "changed"
+++

## changed(a: 'a) 🡒 boolean, ordered aggregator

The aggregator returns `true` for the first line of each group, and for each line that is different from the previous one. It requires an ordering option, either `sort` or `scan`.

```envision
table T = with 
  [| as Val |]
  [| "a" |] // changed = true
  [| "a" |]
  [| "b" |] // changed = true
  [| "b" |]
  [| "b" |]
  [| "c" |] // changed = true

show table "" a1b6 with
  T.Val
  changed(T.Val) scan auto
```

This aggregator is intended to facilitate skipping unchanged lines while persisting data, like historical prices.

The `number` variant of this aggregator is equivalent to the user-defined process as defined below:

```envision
def process changed_bis(next: number) default false with
  keep prev = 0
  changed = prev != next
  prev = next
  return argfirst() or changed
```
