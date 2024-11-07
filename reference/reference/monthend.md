+++
title = "monthEnd"
+++

## monthEnd(d: date) 🡒 date, const pure function

Returns the last day of the month that contains the date `d`.

```envision
show summary "" a1a3 with
  monthEnd(date(2019, 12, 28))
  monthEnd(date(2019, 12, 30))
  monthEnd(date(2020, 1, 1))
```

## See also

* [monthStart](../monthstart/)
