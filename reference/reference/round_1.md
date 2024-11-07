+++
title = "round"
+++

There is another function named 'round()' with 2 arguments ([see here](/reference/pqr/round_2/)). 

## round, function

```envision
def pure round(quantity: number): number
```

Returns the entered 'quantity' rounded to the nearest integer. If the fractional part of the 'quantity' is 0.5, the number is rounded to the nearest even integer.

### Example
```envision
show table "" with
  round(0.5) 
  round(0.51) 
  round(1.5)  
  round(4.5)  
  round(-0.5)
  round(-0.51)
  round(-1.5)
```

This outputs the following table:  
| round(0.5) | round(0.51) | round(1.5) | round(4.5) | round(-0.5) | round(-0.51) | round(-1.5) |
|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 4 | 0 | -1 | -2

### Remarks
Calling 'round(x)' or 'round(x, 0)' gives identical results.

#### Rounding method
The rounding method used here is called the bankers’ rounding ([see wikipedia](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even))..

#### Gradient
The gradient associated to 'round()' is 1, instead of 0, as the mathematical definition would suggest. The purpose of this irregular behavior is to facilate the design of discrete policies.

### Recipes and Best Practices
If you want to round numbers displayed in tiles, you should not use the 'round()' function but rather stylecode '[precision](/specifications/stylecode/properties/precision/)' or '[minPrecision](/specifications/stylecode/properties/minprecision/)'.

### See also
* [roundNext](/reference/pqr/roundnext/)
* [floor](/reference/pqr/floor/)
* [ceiling](/reference/pqr/ceiling/)