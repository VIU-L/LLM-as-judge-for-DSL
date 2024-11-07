+++
title = "parseNumber"
+++

<!-- significant refactoring is in-progress for 'parseNumber'
https://lokad.atlassian.net/browse/LK-6710

TODO: rewrite 'parseNumber' when refactoring is done. -->

## parseNumber(source: text) 🡒 text, pure function

Converts the text into a number. The parser leverages the number format auto-detection behavior of Envision. If the number cannot be parsed, zero is returned instead.

## parseNumber(source: text, tho: text, dec: text) 🡒 text, pure function

Converts the text into a number using `tho` the specified _thousand separator_ and `dec` the specific _decimal separator.

## See also

* [parseDate](../parsedate/)
* [parseTime](../parsetime/)
* [printTime](../printtime/)
