+++
title = "export"
+++

The `export` keyword exposes an element, introduced inside a module, outside the module. This keyword operates with the keyword [`import`](/reference/ghi/import/) as its counterpart.

## export scalar value

A scalar value can be exported:

```envision
// Module named '/sample/my-module'
export const myHello = "Hello"
```

Then, it can be imported:

```envision
import "/sample/my-module" as M with
  myHello
 
show scalar "" with myHello
```

## export user-defined function

A user-defined function can be exported:

```envision
// Module named '/sample/my-module'
export def pure plusOne(x: number) with
  return x + 1
```

Then, it can be imported:

```envision
import "/sample/my-module" as M with
  plusOne
 
show scalar "" with plusOne(2) // 3
```

## export inline enums
<!-- export the primary dimension isn't supported
https://lokad.atlassian.net/browse/LK-10924 -->
An enum can be exported:

```envision
// Module named 'sample/my-module'
export table enum E = "A", "B"
```

Then, it can be imported:

```envision
import "/sample/my-module" as M with
  E
 
a = enum<<E>>("A")
show scalar "" with text(a)
```

## export table comprehension

A table comprehension can be exported:

```envision
// Module named '/sample/my-module'
export table T = with
  [| as A, as B  |]
  [| 1,    true  |]
  [| 2,    false |]
  [| 4,    true  |]
```

Then, it can be imported:

```envision
import "/sample/my-module" as M with
  T
 
show table "" a1b3 with T.A, T.B
```

## export path schema

A path schema can be exported:

```envision
// Module named '/sample/my-module'
export schema '/sample/products.csv' with
  Product : text
  Color : text
  Price : number
```

When a module is imported, all the path schemas that it exports are automatically imported as well.

```envision
import "/sample/my-module" as M

read '/sample/products.csv' as Products

show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price
```

## export named schema

A named schema can be exported:

```envision
// Module named '/sample/my-module'
export schema Products with
  Product : text
  Color : text
  Price : number
```

Then, it can be imported:

```envision
import "/sample/my-module" as M
 
read "/sample/products.csv" as Products with
  schema M.Products
 
show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price
```
