+++
title = "tryParseWeek"
+++

<!-- internal error on 'tryParseWeek' https://lokad.atlassian.net/browse/LK-8426 -->

## tryParseWeek(source: text, format: text) 🡒 (boolean, number), pure function

Returns a (`boolean`, `number`) tuple. The first argument is the value to be parsed. The second argument is the time format. The returned Boolean flag is `true` if the value has been parsed. The returned number value is non-default only if the parsing succeeded.

Example:

```envision
table T = with
  [| as Id, as Raw, as Format    |]
  [| 1, "202103",   "vvvvww"     |]
  [| 2, "2021-S03", "vvvv-'S'ww" |]
  [| 3, "2021S-03", "vvvv'S'-ww" |]
  [| 4, "2021S03",  "vvvv'S'ww"  |]

T.Ok, T.Parsed = tryParseWeek(T.Raw, T.Format) 

show table "Results" a1e4 with
  T.Id
  T.Raw
  T.Ok
  T.Parsed // 2021-W03
```

More on the format value:

* Supported format text values are `vv` (two-digit ISO year), `vvvv` (four-digit ISO year), `w` (one or two-digit ISO week format) and `ww` (zero-padded two-digit ISO week).
* All other alphabetic characters are reserved. They will cause an error if they are used unquoted. Non-alphabetic characters are treated as if they were quoted.
* Sequences of characters can be quoted by surrounding them in `'`, with a double `''` inside to escape that character itself.

Beware, the standard Gregorian calendar and teh ISO-8601 calendar are different.
