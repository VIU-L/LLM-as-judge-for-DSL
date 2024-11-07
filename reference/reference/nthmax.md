+++
title = "nthmax"
+++

## nthmax(T.value : number; nth : number) 🡒 number

Sorts all the values of `T.Value` in descending order, and returns the `nth` one.

`nth` should be an integer between 1 and 100&nbsp;000. 

If there are fewer than `nth` values provided, the function returns the smallest value. If no values are provided, returns the `default`. 

```envision
table T = with
  [| as A |]
  [| 2    |]
  [| 0    |]
  [| 1    |]
  [| 4    |]
  [| 3    |]

V = nthmax(T.A; 2)

show scalar "2nd highest T.A" with V
```

The value of V above is 3. 

