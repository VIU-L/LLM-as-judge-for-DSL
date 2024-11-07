+++
title = "tryParseTime"
+++

## tryParseTime(source: text, format: text) 🡒 (boolean, number), pure function

Returns a (`boolean`, `number`) tuple. The first argument is the value to be parsed. The second argument is the time format. The returned Boolean flag is `true` if the value has been parsed. The returned number value is non-default only if the parsing succeeded.

Example:

```envision
table T = with
  [| as Id, as Raw |]
  [| 1, "2021-10-0900:01:00"  |]
  [| 2, "2021-12-02 10:15:00" |]
  [| 3, "2022-06-06 06:30:00" |]
  [| 4, "2022-08-30 05:46:00" |]

T.Ok, T.Parsed = tryParseTime(T.Raw, "yyyy-MM-dd HH:mm:ss")

show table "Results" a1e4 with
  T.Id
  T.Raw
  T.Ok
  T.Parsed
```

## See also

* [printTime](../../pqr/printtime/)
