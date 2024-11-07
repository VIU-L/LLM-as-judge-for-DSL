+++
title = "Day"
+++

## Day, special calendar table

The table `Day` is a special calendar table. This table can only be created with `expect [date]` in a `read` block, or by an unfiltering statement with `span date =`. When introduced, the `Day` table always has `date` as its primary dimension (of type `date` too).

With `span`:

```envision
span date = [date(2024, 1, 1) .. date(2024, 2, 28)]
  // 2-space of indent, we are within the 'span' block
  Day.X = random.uniform(1 into Day, 10 into Day)
  show linechart "Daily" with Day.X
```

Or alternatively:

```envision
keep span date = [date(2024, 1, 1) .. date(2024, 2, 28)]
// no indent, as 'keep' is used
Day.X = random.uniform(1 into Day, 10 into Day)
show linechart "Daily" with Day.X
```

A `read` block can also be used to introduce the `Day` table:

```envision
read "/sales.csv" as Sales expect [date] with // implicitely creates 'Day'
  "DateOfSales" as date : date // re-map the column originally named 'DateOfSales' to 'date'
  Qty : number

Day.Qty = sum(Sales.Qty) // 'Sales' is downstream of 'Day'
show linechart "Daily" with Day.Qty
```

The `Day` table cannot be created via the usual means, such as table comprehensions for example.

The [`Week`](/reference/vwx/week) and [`Month`](/reference/mno/month) tables are automatically created alongside `Day`.
