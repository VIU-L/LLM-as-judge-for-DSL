+++
title = "arground"
+++

## arground(a: number) 🡒 number, pure function

Returns the answer to the question _at what point the trailing 1 becomes too small to be worth printing?_, or worse, becomes smaller than the precision of floating-point numbers.

The rule is as follows: if we find `000` or `999` in the decimal expansion of a number, then it should be rounded for display. `arground(5.3001)` and `arground(5.2998)` return 4, suggesting to keep all 4 digits after the decimal point, but `arground(5.30001)` and `arground(5.29998)` return 1, suggesting that to present these numbers as 5.3.  Thus, 5.3001 stays 5.3001; 5.30001 would become 5.3; 5.2998 stays 5.2998; 5.29998 becomes 5.3.

```envision
show summary "Roundings" a1a3 with
  arground(5.3001) as "of 5.3001"
  arground(5.30001) as "of 5.30001"
  arground(5.29998) as "of 5.29998"
```
