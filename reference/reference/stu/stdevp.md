+++
title = "stdevp"
+++

## stdevp(T.a : number) 🡒 number, aggregator

Returns the stand deviation on a population that is assumed to be _entirely observed_. The formula is given by:

$$s = \sqrt{\frac{1}{N} \sum_{i=1}^N  \left\(x_i - \bar{x}\right\)^2 }$$

where $\textstyle\{x_1,\, x_2,\, \ldots,\, x_N\}$ are the observed values of the sample items, $\bar{x}$ is the mean value of these observations, and $N$ is the number of observations in the sample.

Example:

```envision
table T = with
  [| as A, as B |]
  [| 0,   "a"   |]
  [| 0,   "a"   |]
  [| 0,   "b"   |]
  [| 1,   "b"   |]
  [| 2,   "c"   |]

table G[gdim] = by T.B

where T.B != "c"
  show table "" a1b4 with
    gdim
    stdevp(T.A)
    group by gdim
```

The aggregator returns 0 on empty groups.

## See also

* [stdev](../stdev/)
* The [STDEV.P](https://support.office.com/en-ie/article/stdev-p-function-6e917c05-31a0-496f-ade7-4f4e7462f285) function in Excel.
