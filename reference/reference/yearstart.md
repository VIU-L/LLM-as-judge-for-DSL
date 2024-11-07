+++
title = "yearStart"
+++

## yearStart(d: date) 🡒 date, const pure function

Returns the first day of the Gregorian year associated to the date `d`.

```envision
show summary "" a1c2 with
  yearStart(date(2020, 1, 1))
  yearStart(date(2019, 5, 1))
```

## yearStart(m: month) 🡒 date, const pure function

Returns the first day of the Gregorian year associated to the month `m`.

```envision
show summary "" a1c2 with
  yearStart(month(2022, 1))
  yearStart(month(2022, 12))
```

### See also

* [year](../year/).
* [yearEnd](../yearend/).
