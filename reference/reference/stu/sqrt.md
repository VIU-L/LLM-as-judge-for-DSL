+++
title = "sqrt"
+++

<!-- negative inputs not yet disallowed 
https://lokad.atlassian.net/browse/LK-6759 -->

## sqrt(a: number) 🡒 number, const autodiff pure function

Returns the square root of the specified number.

Example:

```envision
x = 4.2
y = sqrt(x)
show scalar "" with y
```

Negative inputs are not allowed and will fail.

## See also

* The [SQRT](https://support.office.com/en-ie/article/sqrt-function-654975c2-05c4-4831-9a24-2c65e4040fdf) function in Excel.
