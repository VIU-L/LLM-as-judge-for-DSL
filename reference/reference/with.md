+++
title = "with"
+++

The keyword `with` is frequently used to terminate a statement in Envision and start a block.

## autodiff .. with, differentiable programming block

The `with` keyword is used to introduce the loss function block used for differentiable programming.

```envision
// My gradient-based square-root finder
autodiff Scalar epochs: 500 learningRate: 0.1 with
  params root2 auto
  loss = (root2^2 - 2)^2 // convex, and minimal at sqrt(2)
  return loss
 
show scalar "" with root2 // 1.41
```

## def .. with, user-defined function block

The `with` keyword is used to introduce the body of a user-defined function, pure and process.

```envision
table T = with
  [| as Id, as X |]
  [| "a", 3 |]
  [| "b", 1 |]
  [| "c", 4 |]

def pure mySum(a : number, b : number) with // pure function block
  return a + b

def process myConcat(a : text, b : text) with // process block
  keep result = ""
  result = "\{result}\{a}\{b}"
  return result

show scalar "" with mySum(3, 2) // 5
show scalar "" with myConcat(T.Id, "x") sort T.X // bxaxcx
```

## montecarlo .. with, Monte Carlo block

The `with` keyword is use to introduce a Monte Carlo block.

```envision
montecarlo 1000 with
  x = random.uniform(-2, 2)        // Randomly sample x in the range [-2, 2]
  value = exp(-x^2)                // Compute f(x) = e^(-x^2)
  sample integral = avg(value * 4) // Average the values and multiply by the range width (4)
show scalar "Estimated Integral" with integral
```

The script approximates $\sqrt{\pi}$ through an integration of $f(x) = e^{-x^2}$ over $[-2, 2]$.

## read .. with, reading file

The keyword `with` introduces a read block that read a file from the filesystem of Lokad.

```envision
read "/suppliers.csv" as Suppliers max 1m with
  SupplierName : text
  Location : text
  Rating : number
 
show table "My Suppliers" a1b3 with
  Suppliers.SupplierName
  Suppliers.Location
  Suppliers.Rating
```

## schema .. with, schema block

The `with` keyword is used to introduce a schema block.

```envision
schema Suppliers with // named schema
  SupplierName : text
  Location : text
  Rating : number
 
schema '/suppliers.csv' with // path schema
  schema Suppliers
 
table Suppliers = with
  [| as SupplierName, as Location, as Rating |]
  [| "Supplier A", "New York", 4.5 |]
  [| "Supplier B", "California", 3.0 |]
  [| "Supplier C", "Texas", 5.25 |]
 
write Suppliers as '/suppliers.csv'
```

## show .. with, tile block

The `with` keyword is used to introduce the columns of a tile:

```envision
table T = with
  [| as Id, as X |]
  [| "a", 3 |]
  [| "b", 1 |]
  [| "c", 4 |]

show table "First tile" with T.Id, T.X // inline definition, comma-separated columns
  
show table "Second tile" with // block definition, newline separated
  T.Id
  T.X
```

## table .. = with, table comprehension

The keyword `with` is used to introduce a table comprehension.

```envision
table T = with // table comprehension
  [| as Id, as X |] // colums
  [| "a", 3 |] // first row
  [| "b", 1 |] // ..
  [| "c", 4 |]

show table "T" with T.Id, T.X
```

## write .. with, writing file

The keyword `with` introduces a write block that writes a file into the filesystem of Lokad.

```envision
table Suppliers = with
  [| as SupplierName, as Location, as Rating |]
  [| "Supplier A", "New York", 4.5 |]
  [| "Supplier B", "California", 3.0 |]
  [| "Supplier C", "Texas", -1.0 |]
 
write Suppliers as "/suppliers.csv" with
  SupplierName = Suppliers.SupplierName
  Location = Suppliers.Location
  Rating = if Suppliers.Rating >= 1 and Suppliers.Rating <= 5 then Suppliers.Rating else 2.5
```
