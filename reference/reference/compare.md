+++
title = "comparison operators"
+++

The operators listed below are available for all data types unless specified otherwise.

<!-- Boolean comparison operators missing.
     See https://lokad.atlassian.net/browse/LK-6736
-->

## ('a == 'a) 🡒 boolean, const autodiff

Returns `true` in case of equality.

Text values are compared by Unicode code unit.

```envision
show summary "" a1c4 with
  true == false as "on boolean"
  1 == 2 as "on number"
  "Hello" == "hello" as "on text"
  date(2019,7,1) == date(2019,1,7) as "on date"
```

## ('a < 'a) 🡒 boolean, const autodiff

Returns `true` is the first value is strictly lower than the second one.

Ordering is not available for the `ranvar` and `zedfunc` types.

Text values are sorted in alphabetical order, specifically, by Unicode code points.

```envision
show summary "" a1c4 with
  1 < 2 as "on number"
  "Hello" < "hello" as "on text"
  date(2019,7,1) < date(2019,1,7) as "on date"
```

## ('a != 'a) 🡒 boolean, const autodiff

The expression `a != b` is the same as `not (a == b)`.

```envision
show summary "" a1c4 with
  true != false as "on boolean"
  1 != 2 as "on number"
  "Hello" != "hello" as "on text"
  date(2019,7,1) != date(2019,1,7) as "on date"
```

## ('a > 'a) 🡒 boolean, const autodiff

The expression `a > b` is defined as `not (a < b) and a != b`.

```envision
show summary "" a1c4 with
  1 > 2 as "on number"
  "Hello" > "hello" as "on text"
  date(2019,7,1) > date(2019,1,7) as "on date"
```

## ('a <= 'a) 🡒 boolean, const autodiff

The expression `a <= b` is defined as `(a < b) or a == b`.

```envision
show summary "" a1c4 with
  1 <= 2 as "on number"
  "Hello" <= "hello" as "on text"
  date(2019,7,1) <= date(2019,1,7) as "on date"
```

## ('a >= 'a) 🡒 boolean, const autodiff

The expression `a >= b` is defined as `not (a < b)`.

```envision
show summary "" a1c4 with
  1 >= 2 as "on number"
  "Hello" >= "hello" as "on text"
  date(2019,7,1) >= date(2019,1,7) as "on date"
```
