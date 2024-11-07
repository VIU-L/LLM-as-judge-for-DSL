+++
title = "weekNum"
+++

## weekNum(d: date) 🡒 number, const pure function

Returns the week of the year (1-53) for the date passed as argument. Weeks start on Mondays.

```envision
show summary "" a1a3 with
  weekNum(date(2019, 12, 28))
  weekNum(date(2019, 12, 31))
  weekNum(date(2020, 1, 1))
```

## weekNum(w: week) 🡒 number, const pure function

Returns the week of the year (1-53) for the week passed as argument.

```envision
show summary "" a1a3 with
  weekNum(week(2019, 5))
  weekNum(week(2019, 52))
  weekNum(week(2020, 1))
```

## See also

* [dayNum](../../def/daynum/)
* [monthNum](../../mno/monthnum/)
* The [ISOWEEKNUM](https://support.office.com/en-ie/article/isoweeknum-function-1c2d0afe-d25b-4ab1-8894-8d0520e90e0e) function of Excel.
