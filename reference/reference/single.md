+++
title = "single"
+++

## single(T.'a) 🡒 'a, aggregator

The aggregator fails if any group has more than one element.

Example:

```envision
table T = with
  [| as A, as B |]
  [| 0,   "a"   |]
  [| 1,   "b"   |]
  [| 1,   "c"   |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    single(T.A)
    group by gdim
```

The aggregator `single` succeeds on any empty group, and returns the default value for the given data type.

### See also

* [areSame](../../abc/aresame/).
* [distinct](../../def/distinct/).

## single by, table creation

The contextual keyword `single` modifies the `by` table creation statement. When the modifier `single` is present, the table creation fails if any group has more than 1 element. The vectors of the originating table are copied into the newly created table.

```envision
table T = with
  [| as Code |]
  [| "FR"    |]
  [| "US"    |]
  [| "UK"    |]
  [| "FR"    |] // Fails here due to duplicate

table Countries[c] = single by T.Code

show table "Countries" a1b3 with c
```

The vector copy and the broadcast behavior is illustrated by:

```envision
table T = with
  [| as Code, as X |]
  [| "FR",    1    |]
  [| "US",    2    |]
  [| "UK",    3    |]
  [| "DE",    4    |]

// The vector 'Country.X' is copied from 'T.X' due to 'single'
table Countries[c] = single by T.Code

// The line 'X == 4' is dropped.
show table "Countries" a1b3 with c, Countries.X 
```

In the above script, removing the `single` modifier prevents the script from compiling as `Countries.X` would not exist otherwise.

The `single by` statement is intended as an more readable alternative to a block filter that precisely removes unintended duplicates from the original table.

```envision
table T = with
  [| as Code, as X |]
  [| "FR",    1    |]
  [| "US",    2    |]
  [| "UK",    3    |]
  [| "FR",    4    |]

where T.X != 4
  table Countries[c] = single by T.Code
  Countries.X = T.X 
  show table "" a1b3 with c, Countries.X
```
