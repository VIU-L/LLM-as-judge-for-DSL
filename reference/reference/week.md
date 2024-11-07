+++
title = "week"
+++

## week, data type

The `week` is a primitive data type, representing [ISO weeks](https://en.wikipedia.org/wiki/ISO_week_date) as the combination of a year and a week number within that year, such as `2001-W01` (the earliest week representable in Envision) or `2020-W45`.

```envision
read "/Promo.ion" as Promotions with 
  StartWeek : week
  EndWeek : week
```

Date arithmetic is supported by the `week` type: `weekA + 1` is the week right after `weekA`, and `weekA - weekB` is the number of weeks between `weekA` and `weekB`.

## week(y: number, w: number) 🡒 week, const pure function

Returns a week with ISO week number `w` in year `y` ; will raise an error if the combination is incorrect.

```envision
show scalar "" with 
  week(2020, 45) // 2020-W45
```

## week(d: date) 🡒 week, const pure function

Returns the week associated to the specified date.

```envision
show summary "" a1a3 with
  week(date(2019, 12, 28))
  week(date(2019, 12, 30))
  week(date(2020, 1, 1))
```

## Week, special calendar table

The table `Week` is a special calendar table. This table can only be created with `expect [date]` in a `read` block, or by an unfiltering statement with `span date =`. When introduced, the `Week` table always has `week` as its primary dimension (of type `week` too).

With `span`:

```envision
span date = [date(2024, 1, 1) .. date(2024, 2, 28)]
  // 2-space of indent, we are within the 'span' block
  Week.X = random.uniform(1 into Week, 10 into Week)
  show linechart "Weekly" with Week.X
```

Or alternatively:

```envision
keep span date = [date(2024, 1, 1) .. date(2024, 2, 28)]
// no indent, as 'keep' is used
Week.X = random.uniform(1 into Week, 10 into Week)
show linechart "Weekly" with Week.X
```

A `read` block can also be used to introduce the `Week` table:

```envision
read "/sales.csv" as Sales expect [date] with // implicitely creates 'Week'
  "DateOfSales" as date : date // re-map the column originally named 'DateOfSales' to 'date'
  Qty : number

Week.Qty = sum(Sales.Qty) // 'Sales' is downstream of 'Week'
show linechart "Week" with Week.Qty
```

The `Week` table cannot be created via the usual means, such as table comprehensions for example.

## week, primary dimension

The primary dimension of the table `Week` is named `week`, and it is of type `week`.

```envision
span date = [date(2024, 1, 1) .. date(2024, 2, 28)]
  // 2-space ident, we are within the 'span' block
  Week.X = random.poisson(5 into Week) // 5 is the mean, broadcast into 'Week'
  myWeek = week(2024, 2) // 2nd week of 2024
  show scalar "X on 2nd week" with Week.X[myWeek] // look-up on the primary dimension of 'Week'
```

If a table has `date` as a primary or secondary dimensions, it automatically receives `week` as a secondary dimension as well.
