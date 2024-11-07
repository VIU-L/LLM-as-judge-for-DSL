+++
title = "text"
+++

## text, contextual keyword

The word `text` is a contextual keyword of the Envision language. It refers to the primitive data type `text` that contains a list of Unicode  characters. Text values are capped to 256 characters in Envision.

```envision
tt = "Hello World!"
show table "" write:"/sample/onetext.ion" with tt
```

followed by

```envision
read "/sample/onetext.ion" as T with
  tt : text

show scalar "" a1b2 with same(T.tt)
```

## text(a: 'a) 🡒 text, const pure function

Returns the canonical text representation for all the primitive data types.

```envision
show summary "" a1a4 with
  text(true)
  text(123.45)
  text(date(2020, 8, 27))
  text("Hello World!") // identity
```

The `text()` function is implicitely used when interpolating text value, i.e. `\{myValue}`.

The `text(a: 'a) 🡒 text` is called implicitly when attempting to display a primitive data type.

```envision
a = true
b = 123.45
c = date(2020, 8, 27)
d = "Hello World!"

show summary "" a1a4 with 
  a // implicit 'text(a)'
  b // implicit 'text(b)'
  c // implicit 'text(c)'
  d // already 'text' value
```

## `\{ }`, text interpolation

Text literals benefit for a dynamic behavior called _interpolation_. Interpolation is a syntactic sugar over the concatenation of text values.

```envision
a = 42
b = "bar"
c = date(2022, 2, 17)

x = "\{a} foo \{b} -- \{c}" // interpolate

show scalar "" a1b1 with x // display '42 foo bar -- 2022-02-17'
```

### Interpolation options for dates

Dates can be formatted during the interpolation.

```envision
a = date(2022, 2, 17)
show scalar "" with "\{a:MM/dd/yyyy}" // display '02/17/2022'
```

The available tokens are:

* `d`: day of the month from 1 through 31.
* `dd`: same as `d` but 0 prefixed.
* `ddd`: abbreviated day of the week (ex: Mon, Tue...).
* `dddd`: full day of the week (Monday...).
* `M`: month number from 1 through 12.
* `MM`: same as `M` but 0 prefixed.
* `MMM`: abbreviated name of the month (ex: Jan, Feb, ...).
* `MMMM`: full name of the month (June).
* `yy`: year number from 00 to 99, ignore the hundreds and thousands.
* `yyyy`: year with four digits.

Any other characters are used as in the output text value.
