+++
title = "by"
+++

The `by` keyword serves several purposes in Envision, typically related to grouping lines of an existing table.

## 'table T = by (expr)', table creation

The `by` statement creates a table by grouping the lines of the target vector into group of identical values.

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2022, 9, 13), 3 |]
  [| "orange", date(2022, 9, 14), 2 |]
  [| "apple",  date(2022, 9, 15), 7 |]
  [| "orange", date(2022, 9, 15), 2 |]
  [| "apple",  date(2022, 9, 16), 7 |]

table Products[product] = by Orders.Pid // new table 'Products'

show table "Products" a1b2 with 
  product
  sum(Orders.Quantity) into Products
```

The statement also operates if a tuple is provided.

```envision
table Orders = with
  [| as Pid, as OrderDate, as Quantity |]
  [| "apple",  date(2022, 9, 13), 3 |]
  [| "orange", date(2022, 9, 14), 2 |]
  [| "apple",  date(2022, 9, 15), 7 |]
  [| "orange", date(2022, 9, 15), 2 |]
  [| "apple",  date(2022, 9, 16), 7 |]

table Sales[tu] = by [Orders.Pid, Orders.OrderDate] // new table 'Sales'

Sales.Product, Sales.OrderDate = tu

show table "Sales" a1b5 with 
  Sales.Product
  Sales.OrderDate
  sum(Orders.Quantity) into Sales
```

By construction, if the new table `T` is created from table `U`, then `U` is _upstream_ of `T`.

## 'proc(..) by (expr)', process option

The `by` option is used to control the grouping used by a _process_ (aggregators being the most common processes in Envision).

```envision
table S = with // shipments
  [| as Destination, as Origin, as OrderDate,        as Quantity |]
  [| "USA",         "France",     date(2020, 4, 15), 3           |]
  [| "Germany",     "Spain",      date(2020, 4, 16), 6           |]
  [| "Germany",     "Italy",      date(2020, 4, 16), 2           |]
  [| "USA",         "France",     date(2020, 4, 17), 5           |]
  [| "Germany",     "Spain",      date(2020, 4, 18), 1           |]

// 'by' lets the 'sum' aggregation unfold using 'S.Destination' as the grouping.
// afterward, the results are broadcasted by into the table 'S'.
S.TotalOverTheDestination = sum(S.Quantity) by S.Destination

show table "Shipments" with  S.Destination, S.Origin, S.Quantity, S.TotalOverTheDestination
// Destination,Origin,Quantity,TotalOverTheDestination
// USA,France,3,8
// Germany,Spain,6,9
// Germany,Italy,2,9
// USA,France,5,8
// Germany,Spain,1,9
```

The `at` option can be used to supplement the `by` option, see the `by .. at` below.

## See also

* [Aggregating with an explicit output table](../../../language/relational-algebra/aggregating/#explicit-output-table)
* [by .. at](../../abc/at/)
* [single by (table creation)](../../stu/single/)
* [whichever by (table creation)](../../vwx/whichever/)
