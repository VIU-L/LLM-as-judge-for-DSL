+++
title = "month"
+++

## month, data type

The `month` is a primitive data type, representing months as the combination of a year and a month number within that year, such as `2001-01` (the earliest month representable in Envision) or `2020-10`.

```envision
read "/Promo.ion" as Promotions with 
  StartWeek : month
  EndWeek : month
```

Date arithmetic is supported by the `month` type: `monthA + 1` is the month right after `monthA`, and `monthA - monthB` is the number of months between `monthA` and `monthB`.

## month(y: number, m: number) 🡒 month, const pure function

Returns the month number `m` in year `y` ; will raise an error if the combination is incorrect.

```envision
show scalar "" with 
  month(2020, 10) // 2020-10
```

## month(d: date) 🡒 month, const pure function

Returns the month associated to the specified date.

```envision
show summary "" a1a3 with
  month(date(2019, 12, 28))
  month(date(2019, 12, 30))
  month(date(2020, 1, 1))
```

## Month, special calendar table

The table `Month` is a special calendar table. This table can only be created with `expect [date]` in a `read` block, or by an unfiltering statement with `span date =`. When introduced, the `Month` table always has `month` as its primary dimension (of type `month` too).

With `span`:

```envision
span date = [date(2024, 1, 1) .. date(2024, 4, 28)]
  // 2-space of indent, we are within the 'span' block
  Month.X = random.uniform(1 into Month, 10 into Month)
  show linechart "Monthly" with Month.X
```

Or alternatively:

```envision
keep span date = [date(2024, 1, 1) .. date(2024, 2, 28)]
// no indent, as 'keep' is used
Month.X = random.uniform(1 into Month, 10 into Month)
show linechart "Monthly" with Month.X
```

A `read` block can also be used to introduce the `Week` table:

```envision
read "/sales.csv" as Sales expect [date] with // implicitely creates 'Month'
  "DateOfSales" as date : date // re-map the column originally named 'DateOfSales' to 'date'
  Qty : number

Month.Qty = sum(Sales.Qty) // 'Sales' is downstream of 'Month'
show linechart "Monthly" with Month.Qty
```

The `Month` table cannot be created via the usual means, such as table comprehensions for example.

## month, primary dimension

The primary dimension of the table `Month` is named `month`, and it is of type `month`.

```envision
span date = [date(2024, 1, 1) .. date(2024, 5, 28)]
  // 2-space ident, we are within the 'span' block
  Month.X = random.poisson(5 into Month) // 5 is the mean, broadcast into 'Month'
  myMonth = month(2024, 2) // February of 2024
  show scalar "X in February" with Month.X[myMonth] // look-up on the primary dimension of 'Month'
```

If a table has `date` as a primary or secondary dimensions, it automatically receives `month` as a secondary dimension as well.
