+++
title = "ranvar.segment"
+++

<!-- TODO: 'ranvar.segment' needs a rewrite -->

## ranvar.segment(T.a ..) 🡒 T.r : ranvar, function

Converts time-series into ranvars by collecting observations over moving windows.

```envision-proto
D = ranvar.segment(
  start: Items.Start // first date (inclusive) for each item
  end: Items.End // end date (inclusive) for each item
  step: Items.Step // number, increments in day in-between observation
  horizon: Items.Horizon // number, the length in day of period for each item
  date: Orders.Date  // date for each event
  censoredDemandDate: Censored.Date // days that are skipped when generating the ranvar
  quantity: Orders.Quantity) // quantity for each event
```

This function computes, for each item, the ranvar of the sum of event quantities over periods of horizon length, that are entirely between the first and last date for that item. For example, for a start date on Jan 1st, end date on Jan 7th, a horizon of 3 days, and a single event of quantity 5 on Jan 2nd, the observed periods are:

* Jan 1st - Jan 3rd: Q = 5
* Jan 2nd - Jan 4th: Q = 5
* Jan 3rd - Jan 5th: Q = 0
* Jan 4th - Jan 6th: Q = 0
* Jan 5th - Jan 7th: Q = 0

Thus, the resulting ranvar is 60% Q = 0, 40% Q = 5.

When using the censoredDemandDate: argument, the censored days are skipped, i.e., the ranvar is generated as if these days never existed. Using the previous example, if the 3rd of January is censored, the ranvar segment is applied as if the 4th of January was the day following the 2nd of January.

* Jan 1st - Jan 4rd: Q = 5
* Jan 2nd - Jan 5th: Q = 5
* Jan 4th - Jan 6th: Q = 0
* Jan 5th - Jan 7th: Q = 0

Thus, the resulting ranvar is 50% Q = 0, 50% Q = 5.
