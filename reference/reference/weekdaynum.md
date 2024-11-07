+++
title = "weekDayNum"
draft = true
+++

## weekDayNum(d: date) 🡒 number, pure function

Returns the day of the week (1-7) for the date passed as argument. Weeks start on Mondays.

```envision
span date = [date(2021, 5, 10) .. date(2021, 5, 27)]
  show table "Week Days" a1b10 with
    date
    weekDayNum(date)
```
