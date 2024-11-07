+++
title = "concat"
+++

## concat(T.A : text) 🡒 text, ordered aggregator

The aggregator returns the resulting concatenation of the text values. It requires an ordering option, either `sort` or `scan`.

```envision
table T = with
  [| as A, as B |]
  [| "hello ", "a" |]
  [| "hello ", "a" |]
  [| "hello ", "b" |]
  [| "world",  "b" |]
  [| "world",  "c" |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    concat(T.A) sort T.A
    group by gdim
```

The ordering option can be applied to any ordered data type.

Beware, text values are limited to 256 characters in Envision.

It would also be possible to re-implement `concat` with a user-defined process:

```envision
def process myConcat(a : text) with
  keep c = ""
  if c == ""
    c = a
  else
    c = "\{c}\{a}"
  return c
```

### See also

* [join](../../jkl/join/).

## concat(t: 'a, ...) 🡒 text, const pure function

Returns the concatenation of all the values - of any data types - passed as argument. The function is variadic.

```envision
show summary "" a1d3 with
  concat("0", 1, "2", 3) // returns "0123"
  concat("Hello", " ") // returns "Hello "
  concat("Hello", " ", "World") // returns "Hello World"
  concat("Hello", " ", "World", "!") // returns "Hello World!"
```

All the input values, if not text values already, are converted to text using the `text` function.

This function is similar to the [CONCAT](https://support.office.com/en-ie/article/concat-function-9b1a9a3f-94ff-41af-9736-694cbd6b4ca2) Excel function.

### See also

* [text](../../stu/text/)
