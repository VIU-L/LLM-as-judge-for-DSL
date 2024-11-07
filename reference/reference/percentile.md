+++
title = "percentile"
+++

## percentile(T.a : number; b : number) 🡒 number, aggregator

Returns the value below which the given percentage of observations in the group of observations falls. The second argument must be between 0 and 1 (inclusive). If the percentage falls between two observations, interpolates linearly between the two.

```envision
table T = with
  [| as A |]
  [| 0 |]
  [| 0 |]
  [| 1 |]
  [| 2 |]

show summary "" a1a4 with
  percentile(T.A; 0.25)
  percentile(T.A; 0.50)
  percentile(T.A; 0.75)
  percentile(T.A; 1.0)
```

### See also

* The [PERCENTILE.INC](https://support.office.com/en-us/article/PERCENTILE-INC-function-680F9539-45EB-410B-9A5E-C1355E5FE2ED) function in Excel.

## percentile(T.a : date; b : number) 🡒 date, aggregator

Returns the value below which the given percentage of observations in the group of observations falls. The second argument must be between 0 and 1 (inclusive). If the percentage falls between two observations, interpolates linearly between the two.

```envision
table T = with
  [| as A |]
  [| date(2013,10, 8) |]
  [| date(2016, 7,27) |]
  [| date(2011, 6,11) |]
  [| date(2011, 5,15) |]

show summary "" a1a4 with
  percentile(T.A; 0.25)
  percentile(T.A; 0.50)
  percentile(T.A; 0.75)
  percentile(T.A; 1.0)
```

## percentile(T.a : week; b : number) 🡒 week, aggregator

Returns the value below which the given percentage of observations in the group of observations falls. The second argument must be between 0 and 1 (inclusive). If the percentage falls between two observations, interpolates linearly between the two.

```envision
table T = with
  [| as A |]
  [| week(2013,27) |]
  [| week(2016,13) |]
  [| week(2011, 8) |]
  [| week(2011,11) |]

show summary "" a1a4 with
  percentile(T.A; 0.25)
  percentile(T.A; 0.50)
  percentile(T.A; 0.75)
  percentile(T.A; 1.0)
```

## percentile(T.a : month; b : number) 🡒 month, aggregator

Returns the value below which the given percentage of observations in the group of observations falls. The second argument must be between 0 and 1 (inclusive). If the percentage falls between two observations, interpolates linearly between the two.

```envision
table T = with
  [| as A |]
  [| month(2013,10) |]
  [| month(2016, 7) |]
  [| month(2011, 6) |]
  [| month(2011, 5) |]

show summary "" a1a4 with
  percentile(T.A; 0.25)
  percentile(T.A; 0.50)
  percentile(T.A; 0.75)
  percentile(T.A; 1.0)
```

## percentile(T.a : text; b : number) 🡒 text, aggregator

Returns the value below which the given percentage of observations in the group of observations falls. The second argument must be between 0 and 1 (inclusive). Observations are sorted in lexicographical order. If the percentage falls between two observations, the lower of the two is taken.

```envision
table T = with
  [| as A     |]
  [| "A runner"  |]
  [| "B mainstream" |]
  [| "C slow mover" |]
  [| "D dead stock"   |]

show summary "" a1a4 with
  percentile(T.A; 0.25)
  percentile(T.A; 0.50)
  percentile(T.A; 0.75)
  percentile(T.A; 1.0)
```
