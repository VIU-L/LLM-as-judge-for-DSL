+++
title = "zedfunc"
+++

## zedfunc, contextual keyword

The word `zedfunc` is a contextual keyword of the Envision language. It refers to the primitive data type `zedfunc` that represents a real-valued function over $\mathbb{Z}$.

```envision
z = linear(1) * linear(1) - 1 // f(x) = x^2 - 1  
write Scalar as "/sample/onezedfunc.ion" with 
  MyZedfunc = z
```

followed by

```envision
read "/sample/onezedfunc.ion" as T with
  MyZedFunc : zedfunc

show table "" a1b2 with valueAt(T.MyZedfunc, 3) // 8
```

A zedfunc can be plotted either with `show scalar` or with `show chart`:

```envision
f = linear(2) - 2   // f(x) -> 2x - 2
g = linear(-1) + 3  // g(x) -> 3 - x
fg = f * g

show scalar "Zedfunc: raw" a1c3 with f * g

min = -5
max = 5
table T = extend.range(max - min + 1)
T.X = T.N + min
T.Y = valueAt(fg, T.X)

show chart "Zedfunc: control on boundaries" a4c6 with
  plotxy T.X { as: "myX" }
    T.Y { as: "myY"; color: tomato }
    order by T.X
```
