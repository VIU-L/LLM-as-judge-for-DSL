+++
title = "entropy"
+++

number, date, boolean or text data

## entropy(T.a : 'a) 🡒 number, aggregator

Returns the Shannon Entropy of the group. The value is returned expressed in shannons. The entropy of an empty group is 0. Supported data types are `number`, `text`, `date` and `boolean`.

Example:

```envision
table T = with
  [| as A, as B, as C, as D |]
  [| 0, "a", date(2020, 1, 8) , true |]
  [| 1, "a", date(2010, 9, 1) , true |]
  [| 1, "b", date(2019, 12, 1), true |]

show summary "" a1b4 with
  entropy(T.A)
  entropy(T.B)
  entropy(T.C)
  entropy(T.D)
```

The entropy of an empty group is 0.

The `entropy` aggregator is typically intended to identify the columns of input files with little or no information.

## See also

* [Shannon Entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory))
