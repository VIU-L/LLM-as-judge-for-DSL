+++
title = "const"
+++

## const, keyword, assignment option

The `const` keyword indicates that the value taken by a variable is known at compile time and that it won't change later at runtime. Those variables are primarily intended to control the files being read.

```envision
const myFolder = "/foo"

read "\{myFolder}/products.csv" as Products with // pattern in 'read' must be constant
  Product: text
  Price: number
```

Notably, the `read` block requires a text value for its file path that evaluates as `const`.

Unlike many other languages, in Envision, `const` is a somewhat rarely used keyword, mostly used for certain capabilities that do not accept anything but compile-time constants (ex: `read` blocks).

## const, keyword, pure function option

The `const` keyword indicates that the pure function can be executed at compile time.

```envision
def const pure myInc(a: number) with 
  return a + 1

const a = 42
// if 'myInc' is called with a 'const' input, then, its output is 'const' too
const x = myInc(a)

const myFolder = "/foo"

read "\{myFolder}/products-\{x}.csv" as Products with // pattern in 'read' must be constant
  Product: text
  Price: number
```

In the present reference documentation, pure functions that are part of the Envision standard library and that can be executed at compile time are marked as `const`.
