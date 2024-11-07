+++
title = "yearEnd"
+++

## yearEnd(d: date) 🡒 date, const pure function

Returns the last day of the Gregorian year associated to the date `d`.

```envision
show summary "" a1c2 with
  yearEnd(date(2020, 1, 1))
  yearEnd(date(2019, 5, 1))
```

## yearEnd(m: month) 🡒 date, const pure function

Returns the last day of the Gregorian year associated to the month `m`.

```envision
show summary "" a1c2 with
  yearEnd(month(2022, 1))
  yearEnd(month(2022, 12))
```

### See also

* [year](../year/).
* [yearStart](../yearstart/).
