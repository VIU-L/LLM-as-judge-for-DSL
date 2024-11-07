+++
title = "tryParseDate"
+++

<!-- TODO: rewrite 'tryParseDate' -->

## tryParseDate(source: text, format: text) 🡒 (boolean, date), pure function

The first argument is the value to be parsed.

The second argument is the date format, as documented in function [format()](../../def/format/).

Returns a (`boolean`,`date`) tuple. The returned boolean flag is `true` if and only if the value has been parsed. The returned date value is valid only if the parsing succeeded, its value is unspecified if the parsing failed.

```envision
table T = with 
  [| as text |]
  [| "2022-10-18" |]
  [| "10/18/2022" |] // <- invalid format
  [| "1990-01-01" |] // <- valid format but out of bounds
  [| "2011-05-07" |]

T.ok, T.d = tryParseDate(T.text, "yyyy-MM-dd")
where T.ok
  show table "Parsed" with 
    T.text
    T.d
```

## See also

* [parseDate](../../pqr/parsedate/)
* [parseNumber](../../pqr/parsenumber/)
* [printTime](../../pqr/printtime/)
* [tryParseNumber](../../stu/tryparsenumber/)
