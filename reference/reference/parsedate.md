+++
title = "parseDate"
+++

<!-- significant refactoring has been completed for 'parseDate'
https://lokad.atlassian.net/browse/LK-6710

TODO: rewrite 'parseDate' documentation -->

## parseDate(source: text) 🡒 text, pure function

Converts the text into a date using the default format.

## parseDate(source: text, format: text) 🡒 text, pure function

Converts the text into a date using the specified format. The format is optional. When the format is omitted, the date is parsed based on the date format auto-detection behavior of Envision. When the format is provided, the date is parsed against the format expectation. See custom date format text value for the details of the format syntax. If a date cannot be parsed, the date 2001-01-01 is returned instead.

## See also

* [parseNumber](../parsenumber/)
* [parseTime](../parsetime/)
* [printTime](../printtime/)
* [tryParseDate](../../stu/tryparsedate/)
* [tryParseNumber](../../stu/tryparsenumber/)
