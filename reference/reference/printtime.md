+++
title = "printTime"
+++

<!-- TODO: doc for 'printTime' must be rewritten.
    The dependency to the .NET spec must be eliminated from our spec.
    See https://lokad.atlassian.net/browse/LK-7834 
 -->

## printTime(dayFraction: number) 🡒 text, pure function

Takes a fraction of the day (number between 0 and 1) and returns a text value formatted as `"HH:mm:ss"`.

This function is the reverse of `parseTime(text)`.

## printTime(dayFraction: number, format: text) 🡒 text, pure function

Takes a fraction of the day (number between 0 and 1) returns a text value formatted according to the specified format following [.NET Custom Time Format](https://docs.microsoft.com/en-us/dotnet/standard/base-types/custom-date-and-time-format-strings).

This function is the reverse of `parseTime(text, text)`.

## See also

* [parseDate](../parsedate/)
* [parseNumber](../parsenumber/)
* [parseTime](../parsetime/)
