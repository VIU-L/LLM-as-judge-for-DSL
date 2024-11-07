+++
title = "today"
+++

## today() 🡒 date, const pure function

Returns the current wall-time date according to UTC.

```envision
show scalar "" with today()
```

The function is considered as a compile-time constant, hence, its results
can be used to create a `read` pattern.

## today(timezone: number) 🡒 date, const pure function

Returns the current wall-time date with the time-zone passed as an argument and expressed as the difference in hours to UTC.

```envision
show scalar "" with today(-8) // UTC-8, Los Angeles
```

The function is considered as a compile-time constant, hence, if its argument is a compile-time constant as well,  its results can be used to create a `read` pattern.

```envision
table T = extend.range(23)

T.Offset = T.N - 12

show table "Dates over timezones" a1b10 with
  if T.Offset >= 0 then "UTC+\{T.Offset}" else "UTC\{T.Offset}" as "UTC"
  today(T.Offset)
```

The above script gives the present date over varied timezones.
