+++
title = "quarter"
+++

## quarter(d: date) 🡒 number, pure const function

Returns the quarter of a date. That is, it will return:
 
 - 1 for dates in January, February and March, 
 - 2 for dates in April, May and June, 
 - 3 for dates in July, August and September,
 - 4 for dates in October, November and December.

Example:

```envision
table T = with
  [| as D |]
  [| date(2024,  1,  3) |]
  [| date(2024,  3, 16) |]
  [| date(2023, 11,  2) |]
  [| date(2022,  7, 31) |]

show table "" a1b4 with
  T.D as "Date"
  quarter(T.D) as "Quarter"
```

Will display the table: 

| Date | Quarter |
|---|---|
| 2024-01-03 | 1 |
| 2024-03-16 | 1 |
| 2023-11-02 | 4 |
| 2022-07-31 | 3 |
