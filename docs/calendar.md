+++
title = "Calendar Elements"
description = ""
weight = 14
+++

Historical data is ubiquitous in enterprise software. Envision provides several mechanisms intended to facilitate the processing and visualization of these data. In particular, Envision adopts a calendar-first perspective, which is particularly adapted for most supply chain related undertakings.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Calendar types to store a date, week or month

Envision has three calendar data types: `date`, `week` and `month`. These data types don’t have literals (unlike numbers) but can be instantiated via built-in functions, as illustrated below:

```envision
d = date(2021, 3, 21)
w = week(2021, 20)
m = month(2021, 3)

show summary "Time values" a1a3 with 
  d // 'Mar 21, 2021'
  w // '2021-W11'
  m // '2021-03'
```

In the script above, the variables `d`, `w` and `m` are respectively instantiated via the functions `date()`, `week()` and `month()`.

These built-in functions have the same name as the data type they return. However, these functions also benefit from overloads, notably from `date` conversions:

```envision
d = date(2021, 3, 21)
w = week(d)
m = month(d)

show summary "Time values" a1a3 with 
  d // 'Mar 21, 2021'
  w // '2021-W11'
  m // '2021-03'
```

These calendar types are _absolute_: `month` refers to a specific month in a specific year, not to a month-of-year value on a 1 to 12 scale, idem for `week`. Envision adopts the ISO week date system. The earliest date representable in Envision is the first day of the 21st century, i.e. Monday, January 1st 2001. The last date representable in Envision is 2180-06-06.

The calendar types benefit from arithmetic operations. Integers can be added to or subtracted from calendar values, as illustrated below:

```envision
d = date(2021, 5, 21) + 1
w = week(2021, 20) + 2
m = month(2021, 5) - 3

show summary "Time values" a1a3 with 
  d // 'Mar 22, 2021'
  w // '2021-W22'
  m // '2021-02'
```

Conversely, the difference between two calendar types returns a number representing the time difference, expressed in calendar periods.

```envision
sd = date(2021, 5, 21) - date(2021, 5, 20)
sw = week(2021, 20) - week(2021, 18)
sm = month(2021, 2) - month(2021, 5)

show summary "Time spans" a1a3 with 
  sd // '1'
  sw // '2'
  sm // '-3'
```

Calendar arithmetic is handy to cope with situations that may involve lead times or scheduled operations for example.

Envision includes an extensive support for calendar conversions, e.g. `date(week, dayOfWeek)`, `week(year, weekOfYear)`, and calendar operations, e.g. `monthStart()`, `monday()`. As a rule of thumb, round-trips between text values and calendar values is a strong hint that the script should be rewritten to take advantage of those built-in functions. The [list of functions](/reference/#functions) of the reference section compiles all the calendar-related built-in functions.

_Advanced remark:_ Under the hood, the Envision runtime extensively leverages those specialized data types to speed up the computation. Indeed, generic programming languages typically promote complex _date time_ values, which are not only encompassing the time of day but also the timezone. Date arithmetics are frequently used in supply chain, and these computations end up being accidentally expensive due to the introduction of irrelevant concerns. Even basic sorting operations can be vastly accelerated by the use of specialized algorithms such as _bucket sort_, which vastly outperforms _quick sort_ whenever the number of distinct elements to be sorted is low - as it happens to be the case with distinct calendar values.

### Parsing and printing dates
<!-- Fix is still in progress https://lokad.atlassian.net/browse/LK-6710 -->
As a rule of thumb, in Envision, dates are intended to be parsed via [read statements](/language/files/read-formats/). The display of dates is intended to be controlled via the StyleCode capabilities of Envision. However, Envision also features a few capabilities to control the explicit conversion from `text` values to calendar values and vice versa.

```envision
d = date(2021, 3, 21)
w = week(2021, 20)
m = month(2021, 5)

show summary "Time values" a1a3 with 
  text(d) // '2021-03-21'
  text(w) // '2021-W20'
  text(m) // '2021-05'
```

Conversely,  the `parseDate()` function parses `text` values  into `date` values:

```envision
d = parseDate("2021-03-21")
show scalar "Parsed date" with d // 'Mar 21, 2021'
```

The two functions `text(date)` and `parseDate()` are symmetrical. An [overload of parseDate()](/reference/pqr/parsedate/) is also available to specify the date format.

Also, the `tryParseDate()` function offers a greater degree of control when it comes to the processing of potentially invalid data entries as illustrated by:

```envision
table E = with
  [| as Raw       |]
  [| "2021-02-11" |]
  [| "2021-02-31" |] // no such date
  [| "123"        |] // not a date

E.CanBeParsed, E.ParsedDate = tryParseDate(E.Raw, "yyyy-MM-dd")

show table "Parsing results" a1c3 with
  E.Raw
  E.CanBeParsed
  E.ParsedDate
```

When a date cannot be parsed, the default date `2001-01-01` is returned instead.

_Roadmap:_ We suggest not to rely on the default value `2001-01-01` in the case of failed parsing. Indeed, later evolutions of Envision will probably prevent, by design, to even access unparsable entries. This design angle is unlikely to be specific to the `tryParseDate` function however.

### Time of day and time zones

At this point, Envision remains with limited support for time-of-day values. This limitation reflects Envision’s original intent to support _supply chain_ decisions where there is frequently little to gain by going beyond the daily granularity.  Nevertheless, time-of-day can be processed as illustrated by:

```envision
show table "Time of day" a1b2 with
  parseTime("2021-01-01 12:00:00") as "parseTime" // '0.5'
  printTime(0.5, "HH:mm:ss") as "printTime" // '12:00:00'
```

Time zones are also supported. Envision adopts a UTC-centric perspective as illustrated by:

```envision
show table "Time of day" a1b2 with
  parseDate("2021-01-01 23:00:00 -6", "yyyy-MM-dd HH:mm:ss z") as "parseDate" // Jan 2, 2021
  parseTime("2021-01-01 23:00:00 -6", "yyyy-MM-dd HH:mm:ss z") as "parseTime" // '0.21'
```

In the above script, the date gets parsed as _Jan 2nd_ (instead of _Jan 1st_) due to the specified timezone. Correspondingly, the time of day fraction is parsed as 0.21, which matches the date of Jan 2nd.

## Calendar tables; time series

Calendar tables facilitate the processing of historical dates by offering a mechanism to “densify” the sequences. Indeed, processing and visualizing time-series is typically easier when the time-series are dense.

Let’s start by creating a small flat file containing dates. This flat file will be used in the following to clarify the intent associated with calendar tables:

```envision
table Orders = with
  [| as OrderDate, as Quantity |]
  [| date(2021, 1, 2),   1 |]
  [| date(2021, 1, 3),   2 |]
  [| date(2021, 1, 5),   2 |]
  [| date(2021, 1, 5),   1 |]
  [| date(2021, 1, 9),   2 |]
  [| date(2021, 1, 12),  2 |]
  [| date(2021, 1, 17),  1 |]
  [| date(2021, 1, 17),  3 |]

write Orders as "/sample/orders.csv" with
  OrderDate = Orders.OrderDate
  Quantity = Orders.Quantity
```

The above script creates a file named `orders.csv`, and it only needs to be run once.

Now, let’s consider the following script, which displays the aggregated daily quantities as read from the orders:

```envision
read "/sample/orders.csv" as Orders with
  OrderDate : date
  Quantity : number

show table "Daily Orders" a1b5 with
  Orders.OrderDate
  sum(Orders.Quantity)
  group by Orders.OrderDate
```

As expected, the table puts on display all the dates that originally appear in the `orders.csv` file. However, the dates that were absent from the original entries, such as January 4th, 2021, are missing and appear as gaps in the table.

Yet, from a time-series perspective, it would be of high interest to “fill in” those gaps, in order to display a contiguous list of dates from January 2nd to January 17th. The special table `Day` and its primary dimension `date` support this undertaking:

```envision
read "/sample/orders.csv" as Orders expect [date] with
  "OrderDate" as Date : date
  Quantity : number

show table "Daily Orders" a1b8 with
  date
  sum(Orders.Quantity)
  group by date
```

In the above script, the table displays all the dates from January 2nd to January 17th, including those that do not appear in the `orders.csv` file. When writing `expect [date]`, the construct `[date]` refers to the implicitly defined `Day` table, which happens to have a primary dimension named `date`. This primary dimension also happens to have the `date` data type.

The involvement of the `Day` table can be made more explicit. The following script is strictly equivalent to previous one:

```envision
read "/sample/orders.csv" as Orders expect [date] with
  "OrderDate" as Date : date
  Quantity : number

Day.Quantity = sum(Orders.Quantity)

show table "Daily Orders" a1b8 with
  date
  Day.Quantity
```

In the above script, the variable `Day.Quantity` is a vector that contains the daily quantities. The aggregation from the table `Orders` to the table `Day` is possible, because `date` is the primary dimension of the table `Day` and because the table `Orders` declares `date` as one of its own dimensions.

The need for a dense (i.e. non-sparse) time dimension becomes more obvious when opting for a line chart display, as illustrated by:

```envision
read "/sample/orders.csv" as Orders expect [date] with
  "OrderDate" as Date : date
  Quantity : number

Day.Quantity = sum(Orders.Quantity)

show linechart "Daily Orders" a1c2 {seriesType: "stack"} with 
  Day.Quantity
```

The above script displays the line chart of the daily order quantities. The expression `{seriesType: "stack"}` is a StyleCode fragment that controls the display of the linechart. This topic will be revisited in greater detail in a later section.

Performing a weekly aggregation instead of a daily one is straightforward, as illustrated by:

```envision
read "/sample/orders.csv" as Orders expect [date] with // setup the tables 'Day', 'Week' and 'Month'
  "OrderDate" as Date : date
  Quantity : number

Week.Quantity = sum(Orders.Quantity)

show linechart "Weekly Orders" a1c2 {seriesType: "line"} with
  Week.Quantity
```

The `linechart` tile has a native affinity to the three calendar tables `Day`, `Week` and `Month`. This tile cannot display data that originates from other tables. We will be revisiting below in greater detail the line charts’ behavior.

Meanwhile, let’s do a brief recap of the calendar tables:

| Table | Dimension | Data type |
|-------|-----------|-----------|
| Day   | date      | date      |
| Week  | week      | week      |
| Month | month     | month     |

The same word, e.g. `month`, refers to distinct constructs in the Envision language.

The calendar tables cannot be defined with the usual `table T = with ..` syntax. Indeed, this would lead to situations where `Day` is defined with a non-contiguous list of `date` values causing strange behavior for the programmer. Thus, those calendar tables can only be defined either through a `read` block featuring `expert [date]` (as seen above), with with an unfiltering statement (as detailed below).

At this point, there are still a few Envision behaviors that we haven’t covered in regards to the examples introduced in this section. These behaviors will be gradually clarified in the subsections that follow.

### Unfiltering with keyword ‘span’

Unfiltering is a mechanism introduced by Envision to “densify” the calendar dimensions. This mechanism does the opposite of filtering: it _adds_ elements to the table of interest. Unfiltering is usually performed implicitly via `read` statements. However, unfiltering can be performed explicitly with the keyword `span`. Understanding _unfiltering_ facilitates the understanding of some of the `read` behaviors, which are covered in the next section.

Let’s introduce a script with a `span` block:

```envision
table Orders = with
  [| as OrderDate, as Quantity |]
  [| date(2021, 1, 2),   1 |]
  [| date(2021, 1, 3),   2 |]
  [| date(2021, 1, 5),   2 |]
  [| date(2021, 1, 5),   1 |]
  [| date(2021, 1, 9),   2 |]
  [| date(2021, 1, 12),  2 |]
  [| date(2021, 1, 17),  2 |]
  [| date(2021, 1, 17),  1 |]

span date = [min(Orders.OrderDate) .. max(Orders.OrderDate)] // setup the tables 'Day', 'Week' and 'Month'
  expect Orders.date = Orders.OrderDate
  Day.Quantity = sum(Orders.Quantity)
  show linechart "Daily Orders" a1c2 {seriesType: "stack"} with 
    Day.Quantity
```

In the above script, the `span` keyword unfilters the `date` dimension over a segment that exactly matches the dates found in the `Orders` table. The `expect` keyword binds the `date` dimension to the `Orders` table. Through this binding, the entries in the `Orders` table are aggregated into the `Day` table. Finally, a `linechart` tile displays the resulting time-series.

When a `span` block is introduced, the tables `Day`, `Week` and `Month` get implicitly created along with their respective primary dimensions `date`, `week` and `month`.

The keyword `span` introduces a block marked by an extra level of indentation. The unfilter ends when the block is exited. This syntax is aligned with the `where` blocks, which are used to filter tables. The extra level of indentation can be avoided through the keyword `keep`. Once again, the syntax of `span` is aligned with one of the `where` keywords. The above script can be rewritten as:

```envision
table Orders = with
  [| as OrderDate, as Quantity |]
  [| date(2021, 1, 2),   1 |]
  [| date(2021, 1, 3),   2 |]
  [| date(2021, 1, 5),   2 |]
  [| date(2021, 1, 5),   1 |]
  [| date(2021, 1, 9),   2 |]
  [| date(2021, 1, 12),  2 |]
  [| date(2021, 1, 17),  2 |]
  [| date(2021, 1, 17),  1 |]

keep span date = [min(Orders.OrderDate) .. max(Orders.OrderDate)]
expect Orders.date = Orders.OrderDate
Day.Quantity = sum(Orders.Quantity)
show linechart "Daily Orders" a1c2 {seriesType: "stack"} with 
  Day.Quantity
```

The `expect` statement guarantees that all the values found in `Orders.OrderDate` also exist in the `Day` table. If a value happens to be missing, then the execution fails, as illustrated by:

```envision
table Orders = with
  [| as OrderDate, as Quantity |]
  [| date(2021, 1, 2),   1 |]
  [| date(2021, 1, 3),   2 |]
  [| date(2021, 1, 5),   2 |]
  [| date(2021, 1, 5),   1 |]
  [| date(2021, 1, 9),   2 |]
  [| date(2021, 1, 12),  2 |]
  [| date(2021, 1, 17),  2 |]
  [| date(2021, 1, 17),  1 |]

span date = [min(Orders.OrderDate) .. date(2021, 1, 16)]
  expect Orders.date = Orders.OrderDate
  Day.Quantity = sum(Orders.Quantity)
  show linechart "Daily Orders" a1c2 {seriesType: "stack"} with 
    Day.Quantity
```

This above script fails with the error message `Key 2021-01-17 not found in dimension 'date'.` as the `expect` statement is violated.

It is possible to rewrite the above script without the `expect` keyword. However, in this case, the aggregation requires explicit `by at` arguments as illustrated by:

```envision
table Orders = with
  [| as OrderDate, as Quantity |]
  [| date(2021, 1, 2),   1 |]
  [| date(2021, 1, 3),   2 |]
  [| date(2021, 1, 5),   2 |]
  [| date(2021, 1, 5),   1 |]
  [| date(2021, 1, 9),   2 |]
  [| date(2021, 1, 12),  2 |]
  [| date(2021, 1, 17),  2 |]
  [| date(2021, 1, 17),  1 |]

span date = [min(Orders.OrderDate) .. max(Orders.OrderDate)]
  Day.Quantity = sum(Orders.Quantity) by Orders.OrderDate at date
  show linechart "Daily Orders" a1c2 {seriesType: "stack"} with 
    Day.Quantity
```

However, the `by at` behavior is not strictly identical to the one provided by the `expect` statement. In particular, with the `by at` aggregation, lines in the `Orders` table can be silently dropped, as illustrated by:

```envision
table Orders = with
  [| as OrderDate, as Quantity |]
  [| date(2021, 1, 2),   1 |]
  [| date(2021, 1, 3),   2 |]
  [| date(2021, 1, 5),   2 |]
  [| date(2021, 1, 5),   1 |]
  [| date(2021, 1, 9),   2 |]
  [| date(2021, 1, 12),  2 |]
  [| date(2021, 1, 17),  2 |]
  [| date(2021, 1, 17),  1 |]

span date = [min(Orders.OrderDate) .. date(2021,1,16)]
  Day.Quantity = sum(Orders.Quantity) by Orders.OrderDate at date
  show linechart "Daily Orders" a1c2 {seriesType: "stack"} with 
    Day.Quantity
```

In the above script, the last two lines of the `Orders` tables are not part of the aggregation that defines `Day.Quantity`, but the script succeeds nonetheless.

Nevertheless, if filtering the `Orders` table is the intended behavior when binding it to the `Day` table, then it’s better to use a [filtered dimension assignment](/language/relational-algebra/filtering/#filtered-dimension-assignment) as illustrated by:

```envision
table Orders = with
  [| as OrderDate, as Quantity |]
  [| date(2021, 1, 2),   1 |]
  [| date(2021, 1, 3),   2 |]
  [| date(2021, 1, 5),   2 |]
  [| date(2021, 1, 5),   1 |]
  [| date(2021, 1, 9),   2 |]
  [| date(2021, 1, 12),  2 |]
  [| date(2021, 1, 17),  2 |]
  [| date(2021, 1, 17),  1 |]

span date = [min(Orders.OrderDate) .. date(2021,1,16)]
  where Orders.date = Orders.OrderDate
    Day.Quantity = sum(Orders.Quantity)
    show linechart "Daily Orders" a1c2 {seriesType: "stack"} with 
      Day.Quantity
```

_Advanced remark:_ Unfiltering happens implicitly in Envision when exiting every filtered scope introduced by the keyword `where`. At the point of exit, filtered elements are added back to their respective tables. Conceptually, the table `Day` (or `Week`, or `Month`) can be seen as a “complete” table that contains all the calendar elements from 2001 to 2180. This table is initially entirely filtered out, and cannot be used in the script until it gets unfiltered either via a `read` statement or via a `span` statement.

### ‘read’ and auto-unfiltering

The `read` statement comes with calendar-specific behaviors whenever a column named `date` is present. These behaviors are syntactic sugars that reduce the amount of code boilerplate that would otherwise have to be added to achieve the same effect. Let’s consider:

```envision
read "/sample/orders.csv" as Orders with // no calendar table's setup as there is no 'expect [date]'
  OrderDate : date
  Quantity : number

keep span date = [min(Orders.OrderDate) .. max(Orders.OrderDate)]
keep where Orders.date = Orders.OrderDate

show linechart "Daily Orders" a1c2 {seriesType: "stack"} with 
  sum(Orders.Quantity)
  group into Day
```

In the above script, the two lines `keep span` and `keep where` represent the “boilerplate”, which enables the aggregation from `Orders` into `Day`, which happens within the declaration of the `linechart`.

However, renaming `OrderDate` into `Date` triggers the calendar-specific behaviors and removes the need for those two lines. The following script is strictly identical to the previous one:

```envision
read "/sample/orders.csv" as Orders expect [date] with
  "OrderDate" as Date : date
  Quantity : number

show linechart "Daily Orders" a1c2 {seriesType: "stack"} with 
  sum(Orders.Quantity)
  group into Day
```

In the above script, the `read` block includes a declaration of `date` as a table dimension, and a corresponding renaming of `OrderDate` as `Date`. The unfiltering and the dimension bidding happen implicitly.

If multiple tables are read with `Date` columns, then unfiltering covers a segment ranging from the earliest date to the latest, as observed across all the `Date` columns.

Auto-unfiltering is handy, but can also inadvertently mask data problems, such as entries too far in the past or too far into the future. The [table sizes](/language/relational-algebra/table-sizes/) can be used to mitigate this problem, as illustrated by:

```envision
read "/sample/orders.csv" as Orders expect [date] with
  "OrderDate" as Date : date
  Quantity : number

expect table Day max 100 // 'Day' is capped to 100 lines

show linechart "Daily Orders" a1c2 {seriesType: "stack"} with 
  sum(Orders.Quantity)
  group into Day
```

In the above script, the keyword `expect` enforces a size limit at 100 on the table `Day`. The script fails at runtime if entries found in the `orders.csv` file span over a period greater than 100 days.

There are few supply chain situations that really call for more than 2500 days - i.e. a bit more than 6 years. Thus, it is considered a good practice to limit, on purpose, the size of the `Day` table. Surprisingly old data (conversely future data) is usually a sign of an earlier data preparation problem that needs to be addressed.

### Filtering calendar tables

Calendar tables are dependent on one another. Hence, filtering one calendar table impacts the other calendar tables. This behavior is illustrated by:

```envision
keep span date = [date(2021, 1, 1) .. date(2021, 3, 31)]

where month >= month(date(2021, 2, 1))
  show table "Days" a1b6 with date    // 'Feb 1, 2021' to 'Mar 31, 2021' (inclusive)
  show table "Weeks" c1d6 with week   // '2021-W05' to '2021-W13' (inclusive)
  show table "Months" e1f6 with month // '2021-02' to '2021-03' (inclusive)
```

In the above script, the filter is applied on `month`, the primary dimension of the table `Month`. Yet, the `table` display indicates that the primary dimension `week` of table `Week` has been filtered out with the values `2021-W01` to `2021-W04`; idem, for `date` and `Day`.

The two tables `Week` and `Month` depend on the table `Day`. When `Month` is filtered, then the corresponding `Day` lines are filtered to. In turn, if there is not a single `Day` line matching a given `Month` line, then this line gets filtered out as well.

## Calendar cross tables; Concurrent time-series

Concurrent time-series are of prime interest. Envision approaches those series through the angle of the cross tables, which represent a Cartesian product between a calendar table and another table. The following script builds a mock set of time-series, and puts them on display via Envision’s slicing mechanic:

```envision
table Products[product] = with
  [| as Product, as Factor |]
  [| "cap",      1         |]
  [| "pant",     2         |]
  [| "shirt",    4         |]

keep span date = [date(2021, 1, 1) .. date(2021, 3, 31)]

table P = cross(Products, Day)

// Made-up quantities varying per product and per date
P.Quantity = (date - date(2021, 1, 1)) * Products.Factor

table Slices[slice] = slice by product title: Products.Product
P.slice = Products.slice

show linechart "Sliced" a1d6 slices: P.slice with sum(P.Quantity)
```

In the above script, the table `P` is defined as a cross table between `Products` and `Day`. This table is, in essence, the layout of the concurrent time-series. The variable `P.Quantity` varies by product and by date. The expression used for `P.Quantity` makes little sense business-wise, it boils down to an illustration of the syntax that combines lines from `Day` and lines from `Products`. Finally, the `slice` dimension is introduced and injected into the `linechart` time.

The operations on a (calendar) cross table follow the usual principles of Envision, applying the same operations over multiple lines at once. However, the workload for the Envision runtime is strictly proportional to the size of the calendar table. For example, a cross table between 1 million SKUs and 2,000 days yields 2 billion lines. As a rule of thumb, when dealing with large cross tables, it is appropriate to try to filter the dates to avoid needless processing.

## Lag operator; shifting the data time-wise

The operation of shifting the data time-wise is referred to as “lagging”. Lagging is of high interest for situations that involve delays to be modelled. Envision has a built-in lag operator. In order to introduce to this operator, let’s revisit the lookup operator in the context of the calendar tables:

```envision
table Orders = with
  [| as OrderDate,      as Quantity |]
  [| date(2021, 1, 3),  7           |]
  [| date(2021, 1, 11), 5           |]
  [| date(2021, 1, 12), 4           |]

keep span date = [date(2021, 1, 1) .. date(2021, 2, 1)]
keep where Orders.date = Orders.OrderDate

Day.Quantity = sum(Orders.Quantity)

show summary "Lookups" a1c1 with 
  Day.Quantity[date(2021, 1, 10)] as "Jan 10th" // '0'
  Day.Quantity[date(2021, 1, 11)] as "Jan 11th" // '5'
  Day.Quantity[date(2021, 1, 12)] as "Jan 12th" // '4'
```

In the above script, the `Day.Quantity[..]` expression represents lookup operations. The lookup takes a value found in the dimension as argument, and returns the matching value in the vector.

Now, let’s consider a situation where we would like to shift those quantities from +1 day into the future, i.e. shifting `Day.Quantity` to the right. This can be achieved with the lag operator:

```envision
table Orders = with
  [| as OrderDate,      as Quantity |]
  [| date(2021, 1, 3),  7           |]
  [| date(2021, 1, 11), 5           |]
  [| date(2021, 1, 12), 4           |]

keep span date = [date(2021, 1, 1) .. date(2021, 2, 1)]
keep where Orders.date = Orders.OrderDate

Day.Quantity = sum(Orders.Quantity)
Day.Shifted = Day.Quantity[-1] // shift to the right

show summary "Lookups" a1c2 with 
  Day.Shifted[date(2021, 1, 10)] as "Jan 10th" // '0'
  Day.Shifted[date(2021, 1, 11)] as "Jan 11th" // '0'
  Day.Shifted[date(2021, 1, 12)] as "Jan 12th" // '5'
```

In the above script, `Day.Quantity[-1]` represents the lag operation applied to the right of 1 day. If `Day.Quantity[1]` has been written, the shift would have been applied to the left of 1 day.

The amount of lag is expressed by the periodic unit implicitly attached to the calendar table. For example, `Week.Quantity[-1]` would have represented a shift to the right of 1 week.

The syntax of the lag operator is similar to that of the lookup, as brackets are used in both situations. However, the type of argument differs. In the case of the lookup, the type is aligned with the primary dimension of the table, i.e. `date`, `week` and `month`. In the case of the lag, the type of argument is a scalar number.

## Rolling time window with keyword 'over'; moving average
<!-- TODO: screenshots of the linecharts -->
Beyond the lag, it’s frequently useful to perform calculations over a rolling time window. For example, the moving average forecast is one of the simplest use cases of the “rolling window” perspective. Envision provides built-in support for those operations with the `over` aggregation. Let’s consider a 7-day rolling average:

```envision
table Orders = with
  [| as OrderDate,      as Quantity |]
  [| date(2021, 1, 2),  1           |]
  [| date(2021, 1, 4),  1           |]
  [| date(2021, 1, 12), 1           |]
  [| date(2021, 1, 21), 1           |]

keep span date = [date(2021, 1, 1) .. date(2021, 1, 28)]
keep where Orders.date = Orders.OrderDate

Day.Quantity = sum(Orders.Quantity)
Day.MovingAverage = avg(Day.Quantity) over [-6 .. 0]

show linechart "Series" a1d3 with
  Day.Quantity
  Day.MovingAverage { color: red }
```

In the above script, `Day.MovingAverage` represents the average order quantity observed over the last 7 days (present day included). The start and end of the rolling window follow immediately the `over` keyword, i.e. `-6` and `0` respectively. Finally, the two series are plotted via a `linechart` tile.

The rolling window expects integers, and the semantics of these integer arguments is aligned with the semantic of the lag operation, as introduced in the previous section.

The logic can be modified to perform a 7-day average _excluding_ the last day with:

```envision
table Orders = with
  [| as OrderDate,      as Quantity |]
  [| date(2021, 1, 2),  1           |]
  [| date(2021, 1, 4),  1           |]
  [| date(2021, 1, 12), 1           |]
  [| date(2021, 1, 21), 1           |]

keep span date = [date(2021, 1, 1) .. date(2021, 1, 28)]
keep where Orders.date = Orders.OrderDate

Day.Quantity = sum(Orders.Quantity)
Day.MovingAverage = avg(Day.Quantity) over [-7 .. -1]

show linechart "Series" a1d3 with
  Day.Quantity
  Day.MovingAverage { color: red }
```

It is also possible to omit one of the two boundaries:

```envision
table Orders = with
  [| as OrderDate,      as Quantity |]
  [| date(2021, 1, 2),  1           |]
  [| date(2021, 1, 4),  1           |]
  [| date(2021, 1, 12), 1           |]
  [| date(2021, 1, 21), 1           |]

keep span date = [date(2021, 1, 1) .. date(2021, 1, 28)]
keep where Orders.date = Orders.OrderDate

Day.Quantity = sum(Orders.Quantity)
Day.MovingAverage = avg(Day.Quantity) over [.. 0]

show linechart "Series" a1d3 with
  Day.Quantity
  Day.MovingAverage { color: red }
```

In the above script, `[.. 0]` indicates that the rolling window iteratively expands to contain all the past, plus the present day as well.

The `over` does not have to be done from the `Day` table into itself. It can also be done from any table that has a calendar dimension. The following example illustrates the calculation of _latest quantity_:

```envision
table Orders = with
  [| as OrderDate,      as Quantity |]
  [| date(2021, 1, 2),  1           |]
  [| date(2021, 1, 4),  2           |]
  [| date(2021, 1, 12), 1           |]
  [| date(2021, 1, 21), 1           |]

keep span date = [date(2021, 1, 1) .. date(2021, 1, 28)]
keep where Orders.date = Orders.OrderDate

Day.Quantity = sum(Orders.Quantity)
Day.Latest = last(Orders.Quantity) over [.. 0]

show linechart "Series" a1d3 with
  Day.Quantity
  Day.Latest { color: red }
```

