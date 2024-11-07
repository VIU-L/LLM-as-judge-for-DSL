+++
title = "parseTime"
+++

<!-- TODO: doc for 'parseTime' must be rewritten.
    The dependency to the .NET spec must be eliminated from our spec.
 -->

## parseTime(source: text) 🡒 number, pure function

Converts a time of the day into a fraction between 0 and 1, representing a fractional day. The default format `yyyy-MM-dd HH:mm:ss` is used.

## parseTime(source: text, format: text) 🡒 number, pure function

Converts a time of the day into a fraction between 0 and 1, representing a fractional day. Envision is using the [.NET Custom Time Format](https://docs.microsoft.com/en-us/dotnet/standard/base-types/custom-date-and-time-format-strings).

## See also

* [parseDate](../parsedate/)
* [parseNumber](../parsenumber/)
* [printTime](../printtime/)
* [tryParseTime](../../stu/tryparsetime/)
