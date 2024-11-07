+++
title = "round"
+++

There is another function named 'round()' with 1 argument ([see here](/reference/pqr/round_1/)). 

## round, function

```envision
def pure round(quantity: number, digits: number): number
```

Return 'quantity' rounded to 'digits' precision after the decimal point. Values are rounded to the closest multiple of 10 to the power minus 'digits'. If two multiples are equally close, rounding is done toward the even choice.

### Example
```envision
show table "" with
  round(4.33, 0) 
  round(4.33, 1) 
  round(4.33, 2)  
```

This outputs the following table:  
| round(4.33, 0) | round(4.33, 1) | round(4.33, 2) |
|---|---|---|
| 4 | 4.3 | 4.33

### Remarks
Calling 'round(x)' or 'round(x, 0)' gives identical results.

#### Rounding method
The rounding method used here is called the bankers’ rounding ([see wikipedia](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even))..

#### Conversion to Float32
The conversion to Float32 numbers used in Envision (see [here](https://www.h-schmidt.net/FloatConverter/IEEE754.html)) can alter the rounding method. For instance, *0.05* is converted to *0.0500000007* in Float32, and thus 'round(0.05,1)' in Envision will return *0.1* when the expected result was *0.0*.


#### Gradient
The gradient associated to 'round()' is 1, instead of 0, as the mathematical definition would suggest. The purpose of this irregular behavior is to facilitate the design of discrete policies.

### Recipes and Best Practices
If you want to round numbers displayed in tiles, you should not use the 'round()' function but rather stylecode '[precision](/specifications/stylecode/properties/precision/)' or '[minPrecision](/specifications/stylecode/properties/minprecision/)'.

### See also
* [roundNext](/reference/pqr/roundnext/)
* [floor](/reference/pqr/floor/)
* [ceiling](/reference/pqr/ceiling/)