+++
title = "Table sizes"
description = ""
weight = 8
+++

Envision supports very large tables, up to several billion lines, but this comes at a performance cost, and a script left unsupervised where the input dataset steadily grows out of control can end up consuming significant amounts of resources. At the same time, there are several operations which do not support arbitrarily large tables. In order to avoid runtime failures, where the system discovers that a table is too large for a given operation, Envision lets the script author specify the constraint that "this table will be small enough".

**Table of contents**
{{< toc >}}{{< /toc >}}

## Maximum table size

In table definitions, Envision provides the `max <number>` syntax after the table name in order to limit the number of lines in that table. This is supported in three contexts:

```envision
// In a 'read' statement
read "/Items.csv" as Items[id] max 5500 with
  "Id" as id : text
  Label : text
  Category : text
read "/Orders.csv" as SalesOrders expect[id,date] with
  "Id" as id : text
  "Date" as date : date
  Quantity : number

// In any 'table' statement
table Categories[cat] max 100 = by Items.Category

// As a standalone statement
expect table Week max 104
```

This limit is applied at *runtime*: as soon as the number of lines in the table has been determined, an error interrupts the script if that number exceeds the limit. As such, the main purpose of the `max` statement is to serve as a *safeguard* against tables growing beyond the limits that were deemed reasonable when the script was originally written.

In particular, it is recommended to add `expect table` constraints to the `Day`, `Week` or `Month` tables, which have a tendency to grow over time as the order history deepens.

### Abreviated number suffixes

For very high limits, Envision provides helpful numeric suffixes:

* Thousands: `max 1.2k` is equivalent to `max 1200`.
* Millions: `max 31.7m` is equivalent to `max 31700000`.
* Billions: `max 9b` is equivalent to `max 9000000000`.

### Sizes inside `where` and `when` filters

The `expect table` statement can be used to enforce a size limit within a filter. For example:

```envision
table PriceBreaks = with
  [| as Qty, as Price    |]
  [| 1,      10          |]
  [| 10,     9           |]
  [| 100,    7.5         |]

where arglast(PriceBreaks.Qty <= 8) sort PriceBreaks.Qty
  
  // The filter has left at most one line in table PriceBreaks
  expect table PriceBreaks max 1
```

## Small tables

If a table is flagged as *small*, it will support additional operations not available to normal tables. This includes:

* Appearing on the right side of a `cross`,
* Being a `kept` variable in an `each` loop,
* Being a `params` variable in an [`autodiff`](/language/differentiable-programming) block.

To flag the table as *small*, use the `small` keyword in place of `max` when defining a maximum table size:

```envision-proto
// In a 'read' statement
read "/Items.csv" as Items[id] small 5500 expect [supplier] with
  Id : text
  Label : text

// In any 'table' statement
table Categories[cat] small 100 = by Items.Category

// As a standalone statement
expect table Week small 104
```

The table will then count as *small_*, and the Envision compiler will  verify that you respect all the rules for small tables. These are:

 1. A small table may not have more than **100 million** lines.
 2. A small table that contains at least one text vector may not have more than **2.75 million** lines.
 3. A small table that contains at least one ranvar or zedfunc vector may not have more than **1 million** lines.

If a table does not qualify as small due to a vector, the Envision compiler will report which vector.

For your convenience, any table with less than 1 million lines automatically counts as small, whether that limit was enforced by a `max 1m` statement, or because by design the table cannot have more than 1 million lines, such as `Scalar`, `Day`, `Week`, `Month`, `Slices` and `Files`
