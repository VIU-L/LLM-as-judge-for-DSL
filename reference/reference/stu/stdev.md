+++
title = "stdev"
+++

## stdev(T.a : number) 🡒 number, aggregator

Returns the stand deviation on a population. The formula is given by:

$$s = \sqrt{\frac{1}{N - 1} \sum_{i=1}^N  \left\(x_i - \bar{x}\right\)^2 }$$

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
    stdev(T.A)
    group by gdim
```

The aggregator returns 0 on empty groups.

## See also

* [stdevp](../stdevp/)
* The [STDEV](https://support.office.com/en-ie/article/stdev-function-51fecaaa-231e-4bbb-9230-33650a72c9b0) function in Excel.
