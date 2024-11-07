+++
title = "escape"
+++

## escape(source: text) 🡒 text, const

Formats the argument as an Envision text literal, so that it can be directly pasted into an Envision script. 

This is achieved by escaping any special characters inside the text:

 - `\` becomes `\\`
 - `"` becomes `\"`
 - newline characters become `\n`
 - tab characters become `\t`
 - line feed characters become `\r`
 - zero-terminator characters become `\0`

Any characters outside the Unicode range U+0020 to U+007E is formatted as one or more `\uXXXX` sequences, for example: 

 - **€** contains a single code point U+20AC and becomes `\u20AC`
 - ☣ contains two code points U+2623 and U+FE0F and becomes `\u2623\uFE0F`
 - 🟩 contains a single code point U+1F7E9 but since it is greater than U+FFFF, it is cut into [a surrogate pair](https://en.wikipedia.org/wiki/UTF-16#Code_points_from_U+010000_to_U+10FFFF) `\uD83E\uDD78`. 

The escaped text value is then surrounded with `"` characters. For example: 

| `Text` | `escape(Text)` |
|---|---|
| _(empty)_ | `""`
| `ABC` | `"ABC"` |
| `15" Screen` | `"15\" Screen"` |
| <code>&nbsp;Space&nbsp;</code> | `" Space "`
| `Hello 🙂` | `"Hello \uD83D\uDE42"`

The `escape()` function is often used to see **all** the contents of a text value, since the text value may otherwise contain invisible characters or spaces at the beginning or end that would be trimmed by the file or dashboard views. In the escaped text, both invisible characters and surrounding spaces are made visible.

```envision
capital = "Athens"
country = "Greece "
escapedCountry = escape("Greece ")
show scalar "Without `escape()`" a1c1 with "\{capital} is the capital city of \{country}!"
show scalar "With `escape()`" a2c2  with "\{capital} is the capital city of \{escapedCountry}!"
```
