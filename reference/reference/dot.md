+++
title = "(.) dot operator"
+++

## (.) decimal separator

The dot (.) symbol is used as the decimal separator:

```envision
show scalar "My number" with 12.345
```

## (.) dot operator, vector access operator

The dot (.) symbol is used to access a vector contained in a table.

```envision
table T = with
  [| as X |]
  [| 1 |]
  [| 2 |]
  [| 3 |]

show table "" a1a3 with T.X // 'X' belongs to the table 'T'
```

## (.) dot operator, function namespace selector

The dot (.) symbol is used to select the namespace of built-in functions.

```envision
x = random.poisson(5) // function 'poisson' within the namespace 'random'.
show scalar "" with x
```
