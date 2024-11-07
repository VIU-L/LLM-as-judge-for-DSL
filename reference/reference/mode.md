+++
title = "mode"
+++

## mode(T.a : 'a) 🡒 'a, aggregator

Returns the most frequent observed values in the group. In the case of ties, the smallest value - according to the Envision canonical ordering - is returned Supported data types are `number`, `text`, `date` and `boolean`.

```envision
table T = with
  [| as A, as B, as C, as D |]
  [| 0, "a", date(2020, 9, 1) , true |]
  [| 0, "a", date(2020, 9, 1) , true |]
  [| 0, "b", date(2019, 12, 1), true |]
  [| 1, "b", date(2019, 12, 1), true |]

show summary "" a1b4 with
  mode(T.A)
  mode(T.B)
  mode(T.C)
  mode(T.D)
```

The mode of an empty group is the default value for the given data type.

## See also

* The [MODE](https://support.office.com/en-us/article/MODE-function-E45192CE-9122-4980-82ED-4BDC34973120) function in Excel.
