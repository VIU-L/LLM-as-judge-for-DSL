+++
title = "yearISO"
+++

## yearISO(d: date) 🡒 number, const pure function

Return the ISO year as defined by the lead week calendar part of the ISO 8601 date and time standard.

```envision
show summary "" a1a3 with
  yearISO(date(2019, 12, 28))
  yearISO(date(2019, 12, 31))
  yearISO(date(2020, 1, 1))
```

## yearISO(w: week) 🡒 number, const pure function

Return the ISO year as defined by the lead week calendar part of the ISO 8601 date and time standard.

```envision
show summary "" a1a3 with
  yearISO(week(2019, 3))
  yearISO(week(2019, 15))
  yearISO(week(2020, 1))
```
