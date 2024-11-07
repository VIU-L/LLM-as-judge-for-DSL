+++
title = "scatter"
+++

## scatter, tile type

The tile `scatter` is intended to display a set of 2D points. The tile takes exactly two number vectors as argument.

```envision
table T = extend.range(50)
T.X = random.uniform(0 into T, 1) 
T.Y = random.uniform(0 into T, 1) 
show scatter "" a1d6 with 
  T.X 
  T.Y { value { color: #[if T.X > 0.5 then "blue" else "red"] } }
```
