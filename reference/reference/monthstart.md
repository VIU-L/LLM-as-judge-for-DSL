+++
title = "monthStart"
+++

## monthStart(d: date) 🡒 date, const pure function

Returns the first day of the month that contains the date `d`.

```envision
show summary "" a1a3 with
  monthStart(date(2019, 12, 28))
  monthStart(date(2019, 12, 30))
  monthStart(date(2020, 1, 1))
```

## See also

* [monthEnd](../monthend/)
