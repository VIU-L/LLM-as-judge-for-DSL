+++
title = "date"
+++

## date, data type

The word `date` is a contextual keyword of the Envision language. It refers to the primitive data type `date`, which represents an integral date from January 1st, 2001.

```envision
dd = date(2020, 8, 28)
show table "" write:"/sample/onedate.ion" with dd
```

followed by

```envision
read "/sample/onedate.ion" as T with
  dd : date

show scalar "" a1b2 with same(T.dd)
```

## date, dimension

The identifier `date` always refers to the primary dimension of the [built-in `Day` table](/reference/def/date), and is always of type `date`.

## date(year: number, month: number, dayOfMonth: number) 🡒 date, const pure function

Returns the date associated to the specified `year`, `month` and `dayOfMonth` according to the Gregorian calendar.

```envision
show summary "" a1a3 with
  date(2001, 1, 1)
  date(2020, 11, 25)
  date(2040, 6, 13)
```

The following restrictions apply, or the function fails:

* All arguments must be integers
* The year must be in the segment \[2001, 2178\].
* The combination of arguments must be a valid date.

## date(month: month, dayOfMonth: number) 🡒 date, const pure function

Returns the date associated with the specified day within `month`.

```envision
show summary "" a1a3 with 
  date(month(2001, 1), 1)
  date(month(2020, 11), 25)
  date(month(2040, 6), 13)
```

## date(week: week, dayOfWeek: number) 🡒 date, const pure function

Returns the date associated with the specified day within `week` (monday is 1, sunday is 7).

```envision
show summary "" a1a3 with 
  date(week(2001, 1), 1) // 2001-01-01
  date(week(2020, 48), 3) // 2020-11-25
  date(week(2040, 24), 3) // 2040-06-13
```
