+++
title = "at"
+++

The keyword `at` is a process option in Envision.

## 'proc(..) by (expr) at (expr)'

The `by .. at` syntax is a call option is used to control the output table of a process.

```envision
table Origins = with
  [| as Origin |]
  [| "France"  |]
  [| "Italy"   |]
  [| "Spain"   |]

table Routes = with
  [| as Destination, as Origin |]
  [| "USA",         "France"   |]
  [| "Germany",     "Spain"    |]
  [| "Germany",     "Italy"   |]

table Shipments = with
  [| as Destination, as Origin, as OrderDate,      as Quantity |]
  [| "USA",         "France",   date(2020, 4, 15), 3           |]
  [| "Germany",     "Spain",    date(2020, 4, 16), 6           |]
  [| "Germany",     "Italy",    date(2020, 4, 16), 2           |]
  [| "USA",         "France",   date(2020, 4, 17), 5           |]
  [| "Germany",     "Spain",    date(2020, 4, 18), 1           |]

Origins.Incoming = sum(Shipments.Quantity) by Shipments.Origin at Origins.Origin
 
Routes.Incoming = sum(Shipments.Quantity) // implicit line continuation
  by [Shipments.Destination, Shipments.Origin] // tuple with `[.. , ..]`
  at [Routes.Destination, Routes.Origin]

show table "Incoming by Origin" with Origins.Origin, Origins.Incoming
// Origin, Incoming
// France, 8
// Italy, 2
// Spain, 7

show table "Incoming by Route" with Routes.Destination, Routes.Origin, Routes.Incoming
// Destination, Origin, Incoming
// USA, France, 8
// Germany, Spain, 7
// Germany, Italy, 2
```

The `by-at` allows to process the data from a table `T1` to a table `T2` even if the two tables are otherwise unrelated.

The usual intent with Envision is to avoid  `by-at` by leveraging the relationships between the tables.

```envision
table Origins[orig] = with
  [| as orig    |]
  [| "France"  |]
  [| "Italy"   |]
  [| "Spain"   |]

table Shipments = with
  [| as Destination, as Origin, as OrderDate,      as Quantity |]
  [| "USA",         "France",     date(2020, 4, 15), 3           |]
  [| "Germany",     "Spain",      date(2020, 4, 16), 6           |]
  [| "Germany",     "Italy",      date(2020, 4, 16), 2           |]
  [| "USA",         "France",     date(2020, 4, 17), 5           |]
  [| "Germany",     "Spain",      date(2020, 4, 18), 1           |]

expect Shipments.orig = Shipments.Origin // add 'orig' as a secondary dimension to 'Shipments'

Origins.Incoming = sum(Shipments.Quantity) // implicit 'by-at' using the secondary dimension

show table "Incoming by Origin" with orig as "Origin", Origins.Incoming
// Origin, Incoming
// France, 8
// Italy, 2
// Spain, 7
```

Indeed, a script that aggregates data from table `T1` to table `T2` is likely to do so many times. Defining a relationship removes the need to specify the `by-at` every single time.

## See also

* [Aggregating with an explicit output table](../../../language/relational-algebra/aggregating/#explicit-output-table)
* [by (keyword)](../../abc/by/)
