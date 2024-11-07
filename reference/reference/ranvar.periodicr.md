+++
title = "ranvar.periodicr"
+++

## ranvar.periodicr(T.a ..) 🡒 T.r : ranvar, function

Converts time-series into ranvars by collecting observations over moving windows. Generalizes `ranvar.segment` with an horizon expressed as a ranvar and events at the extrema or at the middle of the chosen time interval are equally taken into account:

```envision
table Items[id] = with // 'id' is the primary dimension of 'Items'
  [| as id, as Start, as End, as LeadTime |]
  [| "A",  date(2023,1,3),  date(2023,1,14), 3 |]
  [| "B",  date(2023,1,10), date(2023,1,18), 2 |]
  [| "C",  date(2023,1,20), date(2023,1,25), 4 |]

table Orders = with
  [| as MyId, as MyDate, as Quantity |]
  [| "A",  date(2023,1,5), 5 |]
  [| "A",  date(2023,1,11), 2 |]
  [| "B",  date(2023,1,20), 1 |]

table Censored = with
  [| as MyId, as StockOutDate |]
  [| "B",  date(2023, 1, 3) |]
  [| "B", date(2023, 1, 5) |]

expect Orders.id = Orders.MyId // add 'id' as secondary dimension of 'Orders'
expect Censored.id = Censored.MyId // idem, for 'Censored'

Orders.D = ranvar.periodicr( // beware, it's not 'periodic' but 'periodicr'
  start: Items.Start
  end: Items.End
  horizon: dirac(Items.LeadTime)
  censoredDemandDate: Censored.StockOutDate // optional
  date: Orders.MyDate
  quantity: Orders.Quantity)

where id == "A" // 1 event displayed
  show table "Periodic Demand" a1d4 with
    id
    Orders.MyDate
    Orders.D
```

Indeed, `ranvar.periodicr` considers an infinite repetition of the input data and sums the event quantities over periods of all possible lengths contained in the horizon ranvar. As a consequence, if we consider the example above and we imagine an additional event of quantity 2 on Jan 7th, `ranvar.periodicr` with `dirac(3)` as the horizon would observe the following:

* Jan 1st - Jan 3rd: Q = 5
* Jan 2nd - Jan 4th: Q = 5
* Jan 3rd - Jan 5th: Q = 0
* Jan 4th - Jan 6th: Q = 0
* Jan 5th - Jan 7th: Q = 2
* Jan 6th - Jan 1st: Q = 2
* Jan 7th - Jan 2nd: Q = 7

and returns the ranvar \~28% Q = 0, \~28% Q = 2, \~28% Q = 5, \~14% Q = 7. For comparison, `ranvar.segment` with horizon 3 and step 1 would ignore the last two lines of the above list and return 40% Q = 0, 20% Q = 2, 40% Q = 5.
