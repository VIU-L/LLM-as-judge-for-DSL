+++
title = "Path schemas"
description = ""
weight = 5
+++

A path schema binds one or several files to a list of typed fields. Schemas are used for reading tables from files or writing tables to files, without having to repeat the list of field names every time, and avoiding typos to creep-in in the file paths themselves.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Schema overview

Schemas are intended as a means to stabilize and document the format of the tabular files either written or read by Envision scripts. Schemas help to avoid entire classes of programming mistakes rooted in the file-based interactions between scripts. For example, changing the name of a field in an output file can inadvertently break another script, executed downstream, as an expected field isn’t going to be found anymore. Moreover, if the same file is read in multiple scripts, then the use of a schema can significantly reduce the verbosity of those scripts.

Let’s introduce our first schema, and use it to produce a more concise write statement:

```envision
schema '/sample/products.csv' with
  Product : text
  Color : text
  Price : number

table Products = with
  [| as Product, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]

write Products as '/sample/products.csv'
```

In the above script, the schema `'/sample/products.csv'` is defined with three named and typed fields. The schema definition is introduced by the keyword `schema` followed by a path literal (not to be confused with a text literal). The `write` statement refers to the schema identified through its path, and thus, omits the fields entirely.

The schema can also be used on the read-side:

```envision
schema '/sample/products.csv' with
  Product : text
  Color : text
  Price : number

read '/sample/products.csv' as Products

show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price
```

In the above script, the `read` statement also refers to the schema identified through its path. This allows, again, to omit the fields entirely.

## Field documentation

The fields introduced by a schema can be documented. This documentation becomes available by hovering over the vectors in the scripts that use the schema.

```envision
schema '/sample/products.csv' with
  /// The product identifier.
  Product : text
  /// The 3-letter color code.
  Color : text
  // The VAT-included unit price.
  Price : number
```

In the above script, the comments introduced by `///` are situated above the line that contains the field declaration that each comment is referring to.

## Field renaming

Field's names, as found in files, may not be compatible with Envision's variable names. For example, the name may include a whitespace. Envision provides a mechanism to rename a field.

```envision
schema '/sample/products.csv' with
  Product : text
  Color : text
  Price : number
  VAT : number = read("value added tax") // renaming the field

table Products = with
  [| as Product, as Color, as Price, as VAT |]
  [| "shirt", "white,grey", 10.50, 0.2 |]
  [| "pants", "blue", 15.00, 0.2 |]
  [| "hat", "red", 5.25, 0.2 |]
 
write Products as '/sample/products.csv'
```

In the above script, the `VAT` field is introduced with an assignment `read("value added tax")` that renames the field originally named `value added tax` as `VAT`. Thus, the CSV file produced through the `write` statement below contains a fourth column named `value added tax`.

A file written with a schema can be read with the same schema.

```envision
schema '/sample/products.csv' with
  Product : text
  Color : text
  Price : number
  VAT : number = read("value added tax") // renaming the field

read '/sample/products.csv' as Products

show table "My Products" a1d3 with
  Products.Product
  Products.Color
  Products.Price
  Products.VAT
```

In the above script, the `read` statement finds a column named `value added tax` in the CSV file. This column gets attached to the `VAT` field.

The field renaming mechanism is the canonical example of a field rebinding that happens symmetrically on the write side and on the read side.

Field rebinding is typically intended to cope with field names that are not compatible with the variable naming rules of Envision, but it can also facilitate refactoring operations, removing the need to immediately rewrite the files when the corresponding variable names are changed.

<!-- ## Field rebinding on read -->
<!-- rebind field on read with path schema not implemented
https://lokad.atlassian.net/browse/LK-10928 -->
<!-- ```envision
schema '/sample/products.csv' with
  Product : text
  Color : text
  Price : number
  VAT : number

read '/sample/products.csv' as Products with
  VAT = read("value added tax")

show table "My Products" a1d3 with
  Products.Product
  Products.Color
  Products.Price
  Products.VAT
``` -->

### Field rebinding on write

When writing against a path schema, all the fields specified by the schema are expected to found among the vectors of the table. The mechanism where each schema field gets attached to its counterpart vector is refered to as binding. However, sometimes the vectors present in the table may not exactly match the expectations of the schema. Thus, Envision offers a mechanism to rebind, within the `write` block the fields to newly introduced vectors.

```envision
schema '/sample/products.csv' with
  Product : text
  Color : text
  Size : text
  Price : number

table Products = with                  // 'Size' is missing
  [| as Product, as Color, as Price |]
  [| "shirt", "white,grey", 10.50 |]
  [| "pants", "blue", 15.00 |]
  [| "hat", "red", 5.25 |]

write Products as '/sample/products.csv' with
  Size = "XL"                          // Completing 'Size'
  Color = uppercase(Products.Color)    // Redefining 'Color'
```

In the above script, the `write` block interferes with the binding of two fields. First, the field `Size`, that does not have a counterpart in the table `Products` is assigned a constant text value `"XL"`. Second, `Color` that has a counterpart gets a new one via `uppercase(Products.Color)`.

Field rebinding is a syntactic sugar. This mechanism can alleviate or postpone the need for extensive refactoring of existing scripts when schemas themselves evolve.

_Advance remark:_ There is no _isolated rebinding on read_ because the path schema precisely hint that the files at the specified path follows the structure as specified by the path schema. On the contrary, the [named schema](../named-schemas/), detailed later, offers an isolated rebinding on read, as the named schema isn't coupled with specific files.

## Path literals
<!-- can't isolate the path from the schema declaration
https://lokad.atlassian.net/browse/LK-10917 -->
<!-- Can't isolate the path from the schema declaration
https://lokad.atlassian.net/browse/LK-10917 -->

The _path_ is a special datatype that identifies a file or a list of files inside the Lokad filesystem, and also identifies a schema - as illustrated in the previous section. Path literals should not be confused with text literals.

```envision
const myPath = '/foo.csv' // single-quote delimiters
const MyText = "/foo.csv" // double-quote delimiters
```

For display purposes, path values are automatically converted to text values:

```envision
const myPath = '/foo.csv'
show scalar "" a1 with myPath
```

### Path prefixing
<!-- path reprefixing not working in 'schema' block
https://lokad.atlassian.net/browse/LK-10916 
https://lokad.atlassian.net/browse/LK-10921 -->

Paths support a limited set of operations. Paths prefixing is one of those operations. It offers the possibility to isolate a _prefix folder_ from the rest of the path.

```envision
schema '/sample/products.csv' with
  Product : text
  Color : text
  Price : number

const myFolder = '/sample'

read '\{myFolder}/products.csv' as Products

show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price

write Products as '\{myFolder}/products.csv'
```

In the above script, the variable `myFolder` defines a prefix folder. This variable is used in the `read` and `write` blocks that follows using the `\{..}` inclusion operator.

Beware, the path prefixing operator `\{..}` should not be confused with text interpolation. The operator must be positioned at the beginning of the path.

### Path schema cloning

When working over a draft version of a script, or when working over the next version of a data pipeline, it can be useful to relocate the files being written and read to avoid interfering with the production. Path schema cloning is a mechanism that facilitates such a relocation of files by introducing a schema that only points to a distinct location.

<!-- https://lokad.atlassian.net/browse/LK-12995
The 'max 1000' option should not be required on the code playground. -->
```envision
read '/sample/products.csv' as Products max 1000 // 'read' comes first, cap at 1000 lines

schema '/production/products.csv' with
  Product : text
  Color : text
  Price : number

schema '/sample/products.csv' = '/production/products.csv' // clone one

show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price
```

In the above script, the first schema points to the `/production` folder, which we want to avoid. Thus, a second schema, clone of the first, is introduced at line 6. At line 10, the `read` block refers to the second schema.

In practice, path schema cloning becomes relevant when the schema itself is isolated into a [module](../modules/) and shared between the two environments. The cloning operation allows to preverve the original schema, while changing the path.

Cloning can also be performed over all the schemas sharing the same prefix.

```envision
read '/sample/products.csv' as Products max 1000 // 'read' comes first, cap at 1000 lines

schema '/production/products.csv' with
  Product : text
  Color : text
  Price : number

schema '/sample' = '/production' // clone all starting with /production

show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price
```

In the above script, cloning statement at line 6 refers all the schemas that match the specified path prefix.

This mechanism facilitates the setup of a second flow, typically a "development" flow, beside the "production" one. It minimizes the amount of changes in the Envision code to prevent the secondary flow from interfering with the primary one.

## Parameterized paths

The data of a table can be _partitioned_ into multiple files. Partitioning is primarily intended for scalability purposes. It can be used to reduce bandwidth, by filtering the files themselves through the partition. A parameterized path refers to a list of files - not just a single file - produced through a partitioned write. The parameterized path is used to re-consolidate data originating from multiple files into a single table.

Let's start with a script that partitions a table into multiple files.

```envision
schema '/sample/products-\{Bucket}.csv' with
  Bucket : number
  Product : text
  Color : text
  Price : number

table Products = with
  [| as Product, as Color, as Price, as Bucket |]
  [| "shirt",    "white,grey", 10.50,       1 |]
  [| "pants",    "blue",       15.00,       2 |]
  [| "hat",      "red",         5.25,       3 |]
  [| "hat",      "blue",        5.25,       3 |]

write Products partitioned as '/sample/products-\{..}.csv'
```

In the above script, a schema with a variable named `Bucket` is introduced. This variable has the `number` datatype. The `write` block refers to the schema, replacing the `Bucket` variable by a selector, here `..` that means _capture all numbers_. The keyword `partitioned` indicates that multiple files may be produced by the `write` block. Indeed, this `write` block produces 3 files respectively named `/sample/products-1.csv`, `/sample/products-2.csv` and `/sample/products-3.csv`.

The variable `Bucket` is a _path parameter_ of the path schema.

The files of the partition can, in turn, be read using the same schema.

```envision
schema '/sample/products-\{Bucket}.csv' with
  Bucket : number
  Product : text
  Color : text
  Price : number

read '/sample/products-\{..}.csv' as Products

show table "My Products" a1d4 with
  Products.Bucket
  Products.Product
  Products.Color
  Products.Price
```

In the above script, the `read` block refers to the schema introduced line 1. The `Bucket` value is found both in the file name, and within the file itself.

The acceptable datatypes for path parameters are: `text`, `number`, `date`, `week`, `month`. A single path can include multiple path parameters as long as they are delimited by a separator.

Parameterized paths are to write partitions through `write .. partitioned` statements, and read them afterward. This mechanism is intended to support internal processing steps within an Envision data flow. This mechanism is not intended to consolidate raw multi-file extractions as obtained from a third-party business system.

Two path schemas cannot capture the same file, as this situation is treated by the Envision compiler as an error. This behavior is guaranteed even if parameterized paths are present. If there exist a combination of path parameter values that create a collision between two path schemas, then the script does not compile.

### Path capture and file deletion

All the files captured by the parameterized path get overwritten when writing over the path schema. This point is a subtle but important aspect of the partitioned write.

Let's revisit the first script of the previous section. Let's assume that the 3 files respectively named `/sample/products-1.csv`, `/sample/products-2.csv` and `/sample/products-3.csv` exist in the file system.

```envision
schema '/sample/products-\{Bucket}.csv' with
  Bucket : number
  Product : text
  Color : text
  Price : number

table Products = with
  [| as Product, as Color, as Price, as Bucket |]
  [| "shirt",    "white,grey", 10.50,       1 |]
  [| "pants",    "blue",       15.00,       2 |]

write Products partitioned as '/sample/products-\{..}.csv'
```

The above script overwrites `/sample/products-1.csv` and `/sample/products-2.csv`, but it _deletes_ the file `/sample/products-3.csv`.

Indeed, the _write_ operation with a parameterized path works as follow:

* List all the files that are captured by the pattern.
* Create new files, if needed.
* Overwrite existing files, if needed.
* Prune empty files.

The behavior ensures the symmetry between the _write_ and the _read_ operations. If files, captured by the parameterized path, were left untouched (for example `/sample/products-3.csv`), then the read operation would yield a table that would not be line-wise identical to the table that originally fed to the write operation.

### Bounded paths

The list of files captured by the parameterized path can be constrained through _path bounds_. Let's revisit the script example of the previous section. Let's assume _again_ that the 3 files respectively named `/sample/products-1.csv`, `/sample/products-2.csv` and `/sample/products-3.csv` exist in the file system.

```envision
schema '/sample/products-\{Bucket}.csv' with
  Bucket : number
  Product : text
  Color : text
  Price : number

table Products = with
  [| as Product, as Color, as Price, as Bucket |]
  [| "shirt",    "white,grey", 10.50,       1 |]
  [| "pants",    "blue",       15.00,       2 |]

const lowerIncl = 1  // inclusive lower bound
const higherIncl = 2 // inclusive higher bound
write Products partitioned as '/sample/products-\{lowerIncl..higherIncl}.csv'
```

The above script overwrites `/sample/products-1.csv` and `/sample/products-2.csv`, but it leaves _untouched_ the file `/sample/products-3.csv`. The constant value variables `lowerIncl` and `higherIncl` act as inclusive lower and higher bounds respectively. Indeed, as those bounds are present, the file `/sample/products-3.csv` is not captured by the pattern, and hence, not overwritten.

The bounds must be compile-time constants. However, the bounds are optional, thus, `'/sample/products-\{lowerIncl..}.csv'` and `'/sample/products-\{..higherIncl}.csv'` would also be valid bounded paths. Conversely, the path `'/sample/products-\{..}.csv'` is unbounded (and valid as well).

The bounded path syntax applies to the read side as well.

```envision
schema '/sample/products-\{Bucket}.csv' with
  Bucket : number
  Product : text
  Color : text
  Price : number

const lowerIncl = 1
const higherIncl = 2
read '/sample/products-\{lowerIncl..higherIncl}.csv' as Products

show table "My Products" a1d4 with
  Products.Bucket
  Products.Product
  Products.Color
  Products.Price
```

In the above script, only the files `/sample/products-1.csv` and `/sample/products-2.csv` get read. The content of the file `/sample/products-3.csv` is never touched, as the file gets filtered by the bounded path itself.

In practice, bounded paths are the mechanism which deliver I/O gains. The partitioned writes simply ensure the correctness of the partition while considering repated write operations performed by a flow that produces files "in place" on a schedule.

<!-- ### Bounded paths with inclusion list -->
<!-- most inclusion list examples don't work 
https://lokad.atlassian.net/browse/LK-10937 -->
<!-- An inclusion list can be used instead of a range to constrain the scope a bounded path.

```envision
schema '/sample/products-\{Bucket}.csv' with
  Bucket : number
  Product : text
  Color : text
  Price : number

const myVal = 1
read '/sample/products-\{myVal}.csv' as Products

show table "My Products" a1d4 with
  Products.Bucket
  Products.Product
  Products.Color
  Products.Price
```
--->

## Table size constraint on schema
<!-- max size on schema should allow a warning range ==> TODO: done, to be documented
https://lokad.atlassian.net/browse/LK-10923 -->
Table size limits are used in two ways in Envision. First, those limits unlock certain features that can't operate over arbitrarily large vectors. Second, it avoid accidental performance issues when processing tables are vastly larger than what was expected at the time the script was written.

The declaration of a schema can include a cap on the number of lines of the resulting table.

```envision
schema '/sample/products.csv' max 10 with
  Product : text
  Color : text
  Price : number
```

In the above script, the `max` keyword is followed by the inclusive maximal number of lines to be associated with the path schema. At runtime, if a script attempts to write or read more than 10 lines while the `write` or `read` block are bound to this path schema, then, execution will fail.

<!-- ### File count constraint on read -->

<!-- confusing syntax: max file count vs max line count
https://lokad.atlassian.net/browse/LK-10929 -->

## Enum downcast of a text field

[Enums](../enums/) may provide an increased performance, especially if the cardinality of the field is low (i..e less than 10,000 distinct values). Envision provides a mechanism to downcast a field originally declared as `text` in its schema into an `enum`.

```envision
schema '/sample/products.csv' with
  Product : text
  Color : text
  Price : number

read '/sample/products.csv' as Products with
  Color : table enum Colors

show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price
```

In the above script, `Color` is declared as a `text` field in the `schema` block. The downcast toward an `enum` happens in the `read` block below.

This feature can be combined with the declaration a primary dimension for the `enum` itself, and the declaration of secondary dimension for the table associated to the path schema.

```envision
schema '/sample/products.csv' with
  Product : text
  Color : text
  Price : number

read '/sample/products.csv' as Products expect [color] with
  Color : table enum Colors[color]

show table "My Products" a1b3 with
  Products.Product
  color
  Products.Price
```

In the above script, inside the `read` block, the enum `Colors` gets `color` as its primary dimension. This dimension is set as a secondary dimension of the table `Products` through `expect [color]` on the first line of the `read` block.

## Field aliasing on read

A schema may introduce a field that ends up creating a naming conflict in a script. To mitigate those situations, Envision offers the possibility to alias a field within a `read` block.

```envision
read '/sample/products.csv' as Products max 1000 with // 'read' comes first, cap at 1000 lines
  ColorAlias = Products.Color

schema '/sample/products.csv' with
  Product : text
  Color : text
  Price : number

show table "My Products" a1b3 with
  Products.Product
  Products.ColorAlias
  Products.Price
```

In the above script, `ColorAlias` is introduced within the `read` block as an alias (same datatype, different name) of the original `Color` field.

In order to understand while aliasing can be used to mitigate an actual name conflict, let's introduce a slightly more complex example.

```envision
schema '/T.csv' with
  Id : text

read "/U.csv" as U[Id] with 
  Id : text                  // 'Id' collides with the schema

read '/T.csv' as T[Ref] with 
  Ref = T.Id                 // Aliasing on read 'Id' as 'Ref'
  X : number = 2

show table "T" a1b2 with
  Ref
  T.X
```

In the above script, a path schema is introduced with a field named `Id`. Below, a first `read` block introduces another table - independent from the path schema - that "accidentally" happens to have `Id` as its primary dimension. In the second `read` block, the `Id` field - which would have conflicted with the dimension named `Id` is aliased as `Ref`. This alias serves as the primary dimension of the table `T[Ref]`.

<!-- ## Enums and path schemas -->
<!-- writing enums is not implemented yet
https://lokad.atlassian.net/browse/LK-10943 -->
<!-- 
In the module,

```envision
// In "/samples/my-module"
export table enum Color = "Red", "Blue", "Green"
```

In the script,
```envision
import "/samples/my-module" as M

schema '/sample/products.csv' with
  Product : text
  Color : enum M.Color
  Price : number

table Products = with
  [| as Product, as Color, as Price |]
  [| "shirt", enum<<Color>>("red"), 10.50 |]
  [| "pants", enum<<Color>>("blue"), 15.00 |]
  [| "hat", enum<<Color>>("green"), 5.25 |]

write Products as '/sample/products.csv'
```
-->

## Modules and path schemas

In practice, the path schema is intended to be isolated into a [module](../modules/), in order to avoid duplicating the `schema` block between the two distinct scripts respectively handling the write operation and the read operation.

The path schema must be marked as `export` in the module:

```envision
// Module named '/sample/my-module'
export schema '/sample/products.csv' with
  Product : text
  Color : text
  Price : number
```

Once the module is imported, the path of the `read` block gets matched with the path schema found in the module.

```envision
import "/sample/my-module" as M
 
read '/sample/products.csv' as Products
 
show table "My Products" a1b3 with
  Products.Product
  Products.Color
  Products.Price
```
