+++
title = "scalar"
+++

## Scalar, built-in table

The `Scalar` table is a built-in table that has exactly 1 line. A variable that does not have an explicit table prefix belongs to the `Scalar` table.

```envision
a = 1 // 'a' belongs to the scalar table (no table prefix)
b = "hello world" // scalar table (no table prefix)

table T = extend.range(5) // T has 5 files
T.X = 42 // 'X' is a vector (non-scalar) that belongs the table T.
```

The `Scalar` cannot be filtered, neither with a `where` block, nor with a `when` process option.

The `Scalar` table very rarely appears explicitely in Envision code. The need to explicitely refer to the `Scalar` table is an edge-case in the Envision syntax.

```envision
autodiff Scalar epochs: 500 learningRate: 0.1 with // SGD over the 'Scalar' table
  params a auto // 'a' is learned via differentiable programming + SGD
  s = a * a
  return s

show scalar "" with a // 'a' belongs to the 'Scalar' table
```

## scalar, tile type

The scalar tile is created with `show scalar`:

```envision
show scalar "options" {tileColor: "red" ; unit: "$" } with 123 // {..}, StyleCode
```

Besides numbers, dates, text and booleans, a scalar tile can also be used to display `ranvar` and `zedfunc`. For displaying `ranvar` and `zedfunc`, the tile will result in a histogram or a plot.

```envision
show scalar "Poisson Law" {tileColor: "red"} with poisson(3) // {..}, StyleCode
```
