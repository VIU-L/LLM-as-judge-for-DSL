+++
title = "format"
+++

## format(d: date, pattern: text) 🡒 text, const pure function

The `format` function provides a small formatting framework intended to convert a date its text counterpart. The first argument is the date to be formatted. The second argument is the pattern, a sequence of specifiers used to specify the intended formatting.

```envision
d = date(2022, 9, 26)

show summary "Formats" a1a3 with
  format(d, "yyyy-MM-dd")  // 2022-09-26
  format(d, "M/dd/yy")     // 9/29/22
  format(d, "MMM d, yyyy") // Sept 26, 2022
```

The list of supported specifiers is given below.

| Specifier | Description              | Source     | Match      |
|-----------|--------------------------|------------|------------|
| `y`       | The year from 0 to 99.   | 2019-06-05 | 19         |
| `y`       |                          | 2001-01-28 | 1          |
| `yy`      | The year from 00 to 99.  | 2001-06-05 | 19         |
| `yy`      |                          | 2001-01-28 | 01         |
| `yyy`     | Same as `yyyy`           |            |            |
| `yyyy`    | The 4-digit year.        | 2019-06-05 | 2019       |
| `yyyy`    |                          | 2001-01-28 | 2001       |
| `M`       | The month from 1 to 12.  | 2019-12-05 | 12         |
| `M`       |                          | 2001-01-28 | 1          |
| `MM`      | The month from 01 to 12. | 2019-12-05 | 12         |
| `MM`      |                          | 2001-01-28 | 01         |
| `MMM`     | The abbreviated month.   | 2019-12-05 | Dec        |
| `MMM`     |                          | 2001-01-28 | Jan        |
| `MMMM`    | The full-word month.     | 2019-12-05 | December   |
| `MMMM`    |                          | 2001-01-28 | January    |
| `d`       | The day from 1 to 31.    | 2019-12-05 | 5          |
| `d`       |                          | 2001-01-28 | 28         |
| `dd`      | The day from 01 to 31.   | 2019-12-05 | 05         |
| `dd`      |                          | 2001-01-28 | 28         |
| `ddd`     | The abbreviated weekday. | 2022-09-26 | Mon        |
| `dddd`    | The full-word weekday.   | 2022-09-26 | Monday     |

Any other character, that isn't listed as a specifier, is written to the formatted output.

Some characters are reserved for future use: `w`, `v` and `\`.
