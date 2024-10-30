+++
title = "Named schemas"
description = ""
weight = 6
+++

A named schema is a weaker alternative to the path schema, that does not include a path. While named schemas can be used as a stand-alone mechanism in Envision, they are intended to supplement path schema for composability purposes.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Named schema overview

The typical intended use case for the name schema is to isolate the list of fields for the path itself.

```envision
schema Products with
  Product : text
  Color : text
  Price : number

schema '/sample/products.csv' with
  schema Products

table Products = with
  [| as Product, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]

write Products as '/sample/products.csv'
```

In the above script, the named schema `Products` is introduced, followed by the path schema `'/sample/products.csv'` that references the named schema.

If there is only a single path involved, then, a path schema should be used as there is no point in introducing a named schema. However, if there are several path schemas that happen to have fields in common, then introducing a named schema makes sense.

```envision
schema Products with
  Product : text
  Color : text
  Price : number

schema '/sample/products.csv' with
  schema Products

schema '/sample/products-with-vat.csv' with
  schema Products
  VAT : number

read '/sample/products.csv' as Products

write Products as '/sample/products-with-vat.csv' with
  VAT = 0.2
```

In the above script, two path schemas are introduced. Those path schemas have 3 fields in common. Those common fields are isolated into the `Products` named schema.

## Stand-alone usage

Named schemas can be used in `write` and `read` block much like path schemas. This mechanism is referred to as the _stand-alone_ usage of the named schema, as it does not involve path schemas.

```envision
schema Products with
  Product : text
  Color : text
  Price : number

table Products = with
  [| as Product, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]

write Products as "/sample/products.csv" with
  schema Products
```

In the above script, all the fields listed in the `Products` schema get written to the CSV file. Instead of explicitely referencing the fields, the named schema itself is introduced within the `write` block.

The `read` block benefits for a similar syntax.

```envision
schema Products with
  Product : text
  Color : text
  Price : number

read "/sample/products.csv" as Products with
  schema Products

show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price
```

In the above script, all the fields listed in the `Products` schema are read from the CSV fil. Instead of explicitely referencing the fields, the named schema itself is introduced within the `read` block.

### Incomplete schemas

A named schema specifies a list of fields to be found, but, unlike path schemas, a named schema does not prevent fields from being introduced beyond the named schema itself - both on the write side and on the read side.

```envision
schema Products with
  Product : text
  Color : text

table Products = with
  [| as Product, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]

write Products as "/sample/products.csv" with
  schema Products
  Price = Products.Price
```

The above script introduces a schema named `Products` with two fields `Product` and `Color`. The `write` block includes the schema, but also a third field named `Price`.

This composition mechanism also applies to the read side.

```envision
schema Products with
  Product : text
  Color : text

read "/sample/products.csv" as Products with
  schema Products
  Price : number

show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price
```

The above script introduces a `read` block that includes two fields through the schema - as done on the write side, and a third field `Price`.

### Inline syntax

An inline more concise syntax is available for the `write` block.

```envision
schema Products with
  Product : text
  Color : text
  Price : number

table Products = with
  [| as Product, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]

write Products as "/sample/products.csv" with schema Products
```

Similarly, the `read` block also benefits from an inline syntax.

```envision
schema Products with
  Product : text
  Color : text
  Price : number

read "/sample/products.csv" as Products with schema Products

show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price
```

## Composing named schemas

A schema can include another schema, and both read and write blocks offer the possibility to interleave field references and schema references. Those composition capabilities are intended to address complex scenarios where persisted tables may share subsets of fields.

```envision
schema JustProduct with
  Product : text

schema JustColor with
  Color : text

schema Products with
  schema JustProduct
  schema JustColor
  Price : number

table Products = with
  [| as Product, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]

write Products as "/sample/products.csv" with
  schema Products
```

In the above script, the schema definition block of `Products` includes the two other schemas `JustProduct` and `JustColor` along with the field `Price` listed directly in the block.

The definition of block of a schema can interleave schema-lines and field-lines. However, no duplicate field names are allowed. In particular, this prevents the possibility of redefining a field through successive schema definitions.

This composition mechanism is also available - under a fairly similar syntax - both for read blocks and write blocks. A read block can be composed with a mix of schema-lines and field-lines:

```envision
schema JustProduct with
  Product : text

schema JustColor with
  Color : text

read "/sample/products.csv" as Products with
  schema JustProduct
  schema JustColor
  Price : number

show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price
```

In the above script, in the `read` block, the fields `Product` and `Color` are referred through the schema, while the last field `Price` is explicitly on its own line.

Conversely, a write block can also be composed with a mix of schema-lines and field-lines:

```envision
schema JustProduct with
  Product : text

schema JustColor with
  Color : text

table Products = with
  [| as Product, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]

write Products as "/sample/products.csv" with
  schema JustProduct
  schema JustColor
  Price = Products.Price
```

Duplicated fields are now allowed neither for read blocks nor for write blocks. This restriction extends the restriction defined for schema definition blocks.

## Field renaming

Renaming fields, that we introduced for [path schemas](../path-schemas/), operate in the same way for named schemas.

```envision
schema PartialProducts with
  ProductId : text = read("Product")
  Color : text
  Size : text
 
read "/sample/products.csv" as Products with
  schema PartialProducts
  Price : number
 
show table "My Products" a1c3 with
  Products.ProductId
  Products.Color
  Products.Price
  Products.Size
```

In the above script, the keyword `read` is used inside the `schema` block in order to bind the `ProductId` field to the field named `"Product"`.

### Field rebinding on read

<!-- TODO: 'rebinding on read' is unclear, and needs rewriting, more example -->

An existing file may diverge, field-wise, from the expectations set by a schema. This can happen whenever a schema is modified (but the relevant files are not), or because the file is produced by a third-party. For those situations, the rebinding operation can be specified within the `read` block.

```envision
schema PartialProducts with
  ProductId : text
  Color : text
  Size : text

read "/sample/products.csv" as Products with
  schema PartialProducts with
    ProductId = read("Product")
    Size = "extra large"
  Price : number

show table "My Products" a1c3 with
  Products.ProductId
  Products.Color
  Products.Price
  Products.Size
```

In the above script, the schema specifies two fields `ProductId` and `Size` that are not found in the file `/sample/products.csv` as produced in a previous section. Within the `read` block, the field `ProductId` is assigned the field `"Product"` which requires prefixing the concrete field name with the keyword `read`. Below, the field `Size` is assigned a constant text literal `"extra large"`.

### Field rebinding on write

The rebinding mechanism is also available on the write side. It offers the possibility to delay, or avoid entirely, the refactoring of a script that isn't aligned with the expected names of the colums as found in the file.

```envision
schema PartialProducts with
  Product : text
  Color : text

table Products = with
  [| as Name, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]

write Products as "/sample/products.csv" with
  schema PartialProducts with
    Product = Products.Name
  Price = Products.Price
```

In the above script, the schema `PartialProducts` is referenced within the `write` block. However, the table `Products` does not contain a vector named `Product`, this vector is named `Name`. The assignment `Product = Products.Name` overrides the automatic binding of a vector that would be expected to be named `Products.Product`.

In most situations, rebinding on write can be avoided altogether by performing the relevant assignment before the write block, as illustrated by:

```envision
schema PartialProducts with
  Product : text
  Color : text

table Products = with
  [| as Name, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]

Products.Product = Products.Name

write Products as "/sample/products.csv" with
  schema PartialProducts
  Price = Products.Price
```

However, such a (re)assignment may not be possible if the vector is already assigned with a conflicting data type:

```envision
schema PartialProducts with
  Product : text
  Color : text

table Products = with
  [| as Name, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]

Products.Product = 42

// not possible, mismatching type, number != text
// Products.Product = Products.Name 

write Products as "/sample/products.csv" with
  schema PartialProducts with
    Product = Products.Name
  Price = Products.Price
```

The intent of rebinding on write is to allow the use of the schema in write blocks even if only of the field of the schema happens to collide with an existing vector in the script that does not have the correct semantic with regards to the expectation of the schema. As a guideline, try avoiding those situations. Vectors manipulated in the script should be consistent with the fields exported through the schema. However, the write override offers a local fix if it is not the case.

## Modules and named schemas

A schema is typically intended to be used multiple times - at the very least used twice, once to write the table and once to read the table. In order to achieve the code reuse, schemas can defined in modules and consumed in scripts.

Let’s create a module named `/sample/my-module` with:

```envision
export schema Products with
  Product : text
  Color : text
  Price : number
```

The module contains the named schema definition. The definition is prefixed by the keyword `export` in order to make the schema accessible outside the module itself. This named schema can then be imported from a script:

```envision
import "/sample/my-module" as MyModule

read "/sample/products.csv" as Products with
  schema MyModule.Products

show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price
```

In the above script, the module is imported and referenced as `MyModule`. The declaration `schema MyModule.Products` refers to the `Products` schema to be found in the module referred by the namespace `MyModule`.

**Roadmap:** Envision does not support yet an alternative, and more concise syntax, to reference schemas found in modules. The module has to be explicitly referenced, and schema references require the module reference to be provided as a prefix. However, we are planning to introduce a prefix-free alternative syntax in the future.
