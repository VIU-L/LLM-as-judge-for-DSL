+++
title = "whichever"
+++

## whichever(T.A : 'a) 🡒 'a, aggregator

The aggregator returns one value for each group if the group is not empty.

Example:

```envision
table T = with
  [| as A, as B |]
  [| "hello", "a" |]
  [| "hello", "a" |]
  [| "hello", "b" |]
  [| "world", "b" |]
  [| "world", "c" |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    whichever(T.A)
    group by gdim
```

When the group is empty, the default value for the data type is used.

The result of the `whichever` aggregator is deterministic - i.e. running the script twice over the same data yields the same result - but the ordering of the data cannot be relied upon. This aggregator is intended as a faster alternative to the use of `first` or `last` without introducing an ordering when it is not needed.

### See also

* [first](../../def/first/)
* [last](../../jkl/last/)

### whichever, table creation

The contextual keyword `whichever` modifies the `by` table creation statement. When the modifier `whichever` is present, the table creation discards all lines for every group except 1 line arbitrarily chosen. The vectors of the originating table are copied into the newly created table.

```envision
table T = with
  [| as Code, as X |]
  [| "FR",    1    |]
  [| "US",    2    |]
  [| "UK",    3    |]
  [| "FR",    4    |]

// The vector 'Country.X' is copied from 'T.X' due to 'whichever'
table Countries[c] = whichever by T.Code

// The line 'X == 4' is dropped.
show table "Countries" a1b3 with c, Countries.X 
```

In the above script, removing the `whichever` modifier prevents the script from compiling as `Countries.X` would not exist otherwise.

In practice, it is frequently expected that the `whichever by` construct would happen in a situation where the choice of the duplicate has no effect because all lines are identical across all the vectors (unlike the example above).
