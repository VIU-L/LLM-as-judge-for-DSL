+++
title = "\\{} interpol operator"
+++

## \\{ }, text interpolation operator

The text interpolation operator `\{..}` is used to insert variable values (converted as `text`) into a text value. This operator also serves for text concatenation.

```envision
a = 1
b = true
d = date(2024, 1, 31)

show scalar "" with "\{a}" // 1
show scalar "" with "\{b}" // true
show scalar "" with "\{d}" // 2024-01-31
show scalar "" with "\{a}\{b} // 1true, concatenatiion.
```

Beware: do not forget the `\`, it's `\{..}`.

The text interpolation only works for variables. Interpolating over expressions or over literals is not supported.

The `number` values benefit from extra formatting options `"\{myNumber:000.00}"`. The number format is specified by the token found after the semi-colon.

The `date` values benefit from extra formatting options `"\{myDate:yyyy-MM-dd}"`. The date format is specified by the token found after the semi-colon.

```envision
a = 12.3
d = date(2024, 1, 31)

show scalar "" with "\{a:000.00}" // 012.30
show scalar "" with "\{d:MMM dd, yyyy}" // Jan 31, 2024
```
