+++
title = "Enum Types"
description = ""
weight = 5
+++

Enums are complex data types intended to deliver better compute performance and to achieve a higher degree of programming correctness. An `enum`, shorthand for enumeration, is an immutable collection of text values. In practice, enums are used as a replacement for the `text` primitive data type.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Define an Enum explicitly to store fixed text values

An `enum` can be defined inline while explicitly listing all the allowed text values.
This can be done with a `table enum` statement as illustrated by:

```envision
table enum Countries = "BE", "FR", "UK", "US"

show table "Countries" a1b4 with
  text(Countries.Value)
  "(\{Countries.Label})"

be = enum<<Countries>>("BE")
show scalar "Belgium" c1 with text(be)
```

In the above script, an `enum` named `Countries` is introduced in the first line. The values of the `enum` are displayed by the `table` tile. Finally, a single `text` value is converted to its `enum` counterpart, back to `text` for display within a `scalar` tile.

The call to the function `text(x : enum Countries)` is actually unnecessary in the specific context of a `show` statement. In this context, the conversion is done automatically. Thus, the beginning of the above script could be simplified as:

```envision
table enum Countries = "BE", "FR", "UK", "US"

show table "Countries" a1b4 with
  Countries.Value
  "(\{Countries.Label})"
```

The inline declaration of an enum can also be done over multiple lines:

```envision
table enum Countries =
  "BE"
  "FR", "UK"
  "US"
```

The `table enum Countries` statement creates a series of elements:

1. A data type named `enum Countries`.
2. A table named `Countries` with 1 line per `enum` value.
3. A vector named `Countries.Label` that contains the text values of the `enum`.
4. A vector named `Countries.Value` that contains the values of type `enum Countries`.
5. A special function named `enum<<Countries>>(x : text)` to parse from `text` values.
6. An overload of the `text(x : enum Countries)` function to convert to `text` values.

The `enum` labels are case-sensitive and any white space in the labels is significant. The `enum` values are unordered: they cannot be compared (via `<`) or sorted (via `sort`).

The table named after the `enum` can be used, among other things, to enumerate the values of the `enum` as it is done in the above script through the vector `Countries.Value`.

When defined inline, enums are eagerly processed during the script compilation. Thus, it is possible to have the definition of the enum appear, in the code, below the first use. For example, it is possible to rewrite the script above as:

```envision
show table "Countries" a1b4 with
  Countries.Value // enum auto-converted to text
  "(\{Countries.Label})"

table enum Countries = "BE", "FR", "UK", "US"
```

However, it is advised to keep `enum` declarations above the code that logically depends on  those enums. This feature is intended for specific situations where colocating the declaration of the enum with another part of the script is more readable than an early declaration.

Under the hood, the Envision runtime replaces the `text` labels of an `enum` by compact identifiers, which can be processed more efficiently than `text` values.

As a rule of thumb, once the data preparation is complete, we recommend using enums for most `text` columns of limited cardinality. The detail of the enums’ limitations is given in the following. Enums offer a simple mechanism to avoid entire classes of programming mistakes, for example testing equality between a country code and a currency code.

_Advanced remark:_ Enums represent a special case of what is typically known as a _generic_ type in languages like C# or Java. They are the sole complex data type supported by Envision. The intent behind the Envision enums is to provide type safety to its relational algebra. Envision enums are similar in essence to the PostgreSQL and MySQL enums.

## Define an Enum from a existing table

An `enum` can be defined inline by referencing the values found a vector. This can be done with a `table enum` statement as illustrated by:

```envision
table T = with 
  [| as Country|]
  [| "BE" |]
  [| "FR" |]
  [| "UK" |]
  [| "US" |]

table enum Countries = T.Country
 
show table "Countries" a1b4 with
  text(Countries.Value)
  "(\{Countries.Label})"
 
be = enum<<Countries>>("BE")
show scalar "Belgium" c1 with text(be)
```

In the above script, an `enum` named `Countries` is defined through an assignemment with `T.Country` on the right.

The syntax is essentially similar to the one used for extension enum in the previous section.

## Erasing the original text after creating an Enum

A vector of type `text` can be erased in favor of an `enum` type replacement. This erasure represents an exception to the general Envision rule that prevents an existing vector gaining a new type after being created.

```envision
table enum Countries = "FR", "UK", "DE", "US"

table Factories = with 
  [| as Code, as Country |]
  [| 0,      "US"        |]
  [| 1,      "FR"        |]
  [| 2,      "US"        |]

Factories.Country = enum<<Countries>>(Factories.Country)

show table "Factories" a1b3 with Factories.Code, Factories.Country
```

In the above script, the vector `Factories.Country` is created a `text` vector. This vector is assigned vector of type `enum<<Countries>>`. From this point on, the vector `Factories.Country` is no more a `text` vector; the original type has been erased.

This exception to the general rule of type immutability in Envision is motivated by the frequent use-case where raw data is first read as `text` and second converted as an `enum` after completing miscellaneous preparation steps. Indeed, once the data preparation is complete, the intent is to remove entirely the initial `text` vector, letting a strongly-typed `enum` vector takes its place. This syntax removes the possibility to inadvertently access the original untyped `text` vector after the introduction of a stronger-typed alternative.

## Matching and filtering an Enum

Enums benefit from matching and filtering capabilities that take advantage of their strongly typed nature. The following script illustrates the matching syntax:

```envision
table enum Countries = "BE", "FR", "UK", "US"

x = enum<<Countries>>("UK")

y  = match x with
  "BE" -> 1
  "FR" -> 1 + 1
  "UK" -> 1 + 1 + 1
  "US" -> 1 + 1 + 1 + 1

show scalar "y" with y // displays '3'
```

In the above script, the `match` keyword is used to enumerate the values of the `enum Countries` type. On the left side of the `match`, the `text` literals are automatically converted into enum values in order to test for equality.

If a case is missing, the compilation fails as illustrated:

```envision
table enum Countries = "BE", "FR", "UK", "US"

x = enum<<Countries>>("UK")

y  = match x with
  "BE" -> 1
  "FR" -> 1 + 1
  "UK" -> 1 + 1 + 1 // WRONG! 'match' must include a case for enum value 'US'

show scalar "y" with y
```

However, all cases are not required to be listed explicitly, a fallback can be used with:

```envision
table enum Countries = "BE", "FR", "UK", "US"

x = enum<<Countries>>("UK")

y  = match x with
  "BE" -> 1
  "FR" -> 1 + 1
  "UK" -> 1 + 1 + 1
  .. -> 1 + 1 + 1 + 1

show scalar "y" with y // displays '3'
```

In the above script, the token `..` is used to indicate the case that is selected if none of the previous cases are matching.

The exhaustivity checks provided by Envision for the enums ensure that no case gets accidentally overlooked. This behavior is desirable to avoid certain classes of programming mistakes.

Trying to call the special function `enum<<Countries>>(x : text)` against an invalid value fails. However, it is straightforward to test whether a given text value belongs to an enum:

```envision
table enum Countries = "BE", "FR", "UK", "US"

table Raw = with
  [| as Label  |]
  [| "BE"  |]
  [| "fr"  |]
  [| " US" |]

Raw.IsValid = Raw.Label in Countries.Label

show table "Countries" a1b3 with
  Raw.Label
  Raw.IsValid
```

In the above script, the expression `Raw.Label in Countries.Label` evaluates as a Boolean value, which indicates whether the text value `Raw.Label` belongs to `enum Countries`.

Also, a syntactic sugar, when an enum appears into an (in)equality expression, i.e. a comparison `==` or `!=`, from a semantic perspective, the enum value _appears_ to be automatically converted to a text value to make the comparison possible:

```envision
table enum Countries = "BE", "FR", "UK", "US"

table Details = with
  [| as Label, as Name      |]
  [| "BE", "Belgium"        |]
  [| "FR", "France"         |]
  [| "UK", "United Kingdom" |]

fr = enum<<Countries>>("FR")

where fr == Details.Label // auto conversion to 'text(fr)'
  show table "Countries" a1b2 with
    Details.Label
    Details.Name
```

In particular, this syntax alleviates the need to call the `text()` function on the enum value. Under the hood, the Envision runtime attempts to avoid an actual conversion of the `enum` value to its corresponding `text` value in order to minimize the performance overhead.

## Read and write an Enum from file 

Input files read by an Envision script can declare a column to be of an `enum` type. Moreover, the enums themselves can be defined based on the data observed in input files.  In order to illustrate the affinity between `enum` and the `read` statements, let’s start by producing a flat file:

```envision
table C = with
  [| as Code, as Name       |]
  [| "BE", "Belgium"        |]
  [| "FR", "France"         |]
  [| "FR", "French Guiana"  |]
  [| "UK", "United Kingdom" |]

write C as "/sample/countries.csv" with 
  Code = C.Code
  Name = C.Name
```

The above script writes a list of 4 entries into a flat text file named `countries.csv`. This script only needs to be run once. The following scripts in this section are reading this file.

The column of a table can be typed as an enum. This behavior is of prime interest to ensure that the column does not contain corrupt entries, which would wreak havoc downstream in the script itself.  The following script illustrates how an enum defined inline can be used as a data type in a `read` block:  

```envision
table enum Countries = "BE", "FR", "UK", "US"

read "/sample/countries.csv" as C with
  Code : enum Countries
  Name : text

show table "Countries" a1b3 with
  C.Code
  C.Name
```

The above script uses the syntax `Code : enum Countries` to declare the vector `C.Code` to be typed according to the enum. If the input file `countries.csv` were to contain a country code that wasn’t listed in `enum Countries`, then the read operation would fail at runtime.

However, the validity of an `enum` type found in a `read` block is only checked if the column happens to be used by the Envision script. The following script runs successfully:

```envision
table enum Countries = "BE" // "FR", "UK" missing

read "/sample/countries.csv" as C with
  Code : enum Countries
  Name : text

show table "Countries" a1b3 with C.Name // succeeds
```

The above script succeeds while the file `countries.csv` contains code that is not reflected in the declaration of the enum `Countries` because the vector `C.Code` is never used. As a result, the correctness of the content of the `C.Code` is not checked.

```envision
table enum Countries = "BE" // "FR", "UK" missing

read "/sample/countries.csv" as C with
  Code : enum Countries
  Name : text

show table "Countries" a1b3 with C.Code
```

An enum can also be defined directly from a `read` statement. Instead of explicitly declaring the enum values in the script, the values are extracted from the input files:

```envision
read "/sample/countries.csv" as C with
  Code : table enum Countries
  Name : text

show table "Codes" a1b3 with Countries.Label
show table "Names" c1d3 with C.Name
```

In the above script, the syntax `table enum Countries` is used to introduce the enum named `Countries`. While the table `C` has 4 lines, the table `Countries` has only 3 lines, as the enum represents a collection of distinct text values.

When a `read` block is used to declare an `enum` type, there are no checks involved beyond the capacity limits (see below): the `enum` values are the distinct values observed in the input file. If the input file contains incorrect enum values, those values end up in the definition of the `enum`. However, in practice, a first `read` block can be used to declare an `enum` (this file is assumed to be correct), while a second `read` block consumes the `enum` (the integrity of this file is checked against the first one).

## Using an Enum as Primary dimension of a table

The creation of an enum leads to the creation of a table sharing the same name as its originating enum. This table’s primary dimension has the same type as the enum itself and can be named explicitly:

```envision
table enum Countries[country] = "BE", "FR", "UK", "US"
show table "Countries" a1b4 with country
```

The primary dimension can also be named when the enum is declared as part of a `read` block. Revisiting the flat file `countries.csv` created in the previous section, this can be done with:

```envision
read "/sample/countries.csv" as C with
  Code : table enum Countries[country]
  Name : text

show table "Countries" a1b3 with country
```

It is also possible to use an enum as the primary dimension of the table being read:

```envision
read "/sample/countries.csv" as C[name] with
  Code : text
  Name : table enum

show table "Countries" a1b3 with name
```

In the above script, the type `enum C` is used for the primary dimension of the table `C`. The enum type is assigned through the syntax `table enum`, however, the enum table isn’t anonymous as it’s the table `C` itself.

When the primary dimension of a table is typed as an enum, if duplicate values are found for the enum, then the `read` block fails. This problem is illustrated with:

```envision
read "/sample/countries.csv" as C[code] with
  Code : table enum // Fails due duplicate value 'FR'
  Name : text

show table "Countries" a1b3 with code
```

Whenever a table contains a column that is expected to be a “well-behaved” primary dimension, it is recommended to strong type this dimension as an `enum` in order to benefit from the integrity checks performed by Envision.

### Lookup auto-conversion

A lookup is possible over an enum table. As the primary dimension is the enum type itself, a value of the enum is expected to perform the lookup.

```envision
table enum Countries = "FR", "UK", "DE", "US"
Countries.Selected = random.binomial(0.5 into Countries)
show scalar "Is FR selected?" with Countries.Selected[enum<<Countries>>("FR")]
```

However, if a `text` value is provided to the lookup instead of an enum value, the `text` value is automatically promoted to the enum type that matches the table.

```envision
table enum Countries = "FR", "UK", "DE", "US"
Countries.Selected = random.binomial(0.5 into Countries)
show scalar "Is FR selected?" with Countries.Selected["FR"]
```

This automatic conversion is a syntactic sugar shortening lookups performed over enum tables.

## Using an Enum as Secondary dimension of a table

The enum-typed reads offer the possibility to attach secondary dimensions to the table being read. Let’s produce a minimal flat file illustrating a list of SKUs, each SKU having a location and product reference:

```envision
table SKUs = with
  [| as Loc,    as Ref      |]
  [| "Paris",   "shirt-123" |]
  [| "London",  "shirt-123" |]
  [| "Paris",   "pant-234"  |]
  [| "London",  "hat-345"   |]

write SKUs as "/sample/skus.csv" with
  Loc = SKUs.Loc
  Ref = SKUs.Ref
```

The primary dimensions of the enums declared in the `read` block can be used to assign secondary dimensions to the table being read:

```envision
read "/sample/skus.csv" as SKUs expect [ref] with
  Ref: table enum Ref[ref]
  Loc: table enum Loc

show table "SKUs" a1b3 with ref into SKUs
```

In the above script, the secondary dimension is declared via `expect [ref]` above the code that declares the enums themselves. While there is only a single secondary dimension, the brackets `[]` are mandatory.

The declaration of the secondary dimension with the `expect` keyword is required to benefit from a broadcast relationship between the table being read and the enum table. Without the `expect [ref]`, the above script would fail at compiling the expression `ref into SKUs`.

It is also possible to declare several secondary dimensions:

```envision
read "/sample/skus.csv" as SKUs expect [ref, loc] with
  Ref: table enum Ref[ref]
  Loc: table enum Loc[loc]

show table "SKUs" a1b3 with ref into SKUs, loc
```

<!--
How to import the primary dimension of an enum defined in a module? 
https://lokad.atlassian.net/browse/LK-9996

How to import an enum value from a module?
https://lokad.atlassian.net/browse/LK-9998
-->
## Modules and enums

Enums can be isolated in modules in order to be used in multiple scripts.

```envision
// Module named '/sample/my-module'
export table enum Colors = "Red", "Blue", "Green"
```

In the above module, the `export` keyword is used to indicate that the enum `Colors` becomes accessible to scripts.

```envision
import "/sample/my-module" as M with 
  Colors
red = enum<<Colors>>("Red")
show scalar "My color" with red
```

In the above script, the `import` keyword is used to indicate that enum `Colors` is imported within the script.

## Performance and limitations

An enum is limited to 100 million distinct values and 1 GB of text data, whichever comes first.

From the runtime perspective of Envision, a _small_ vector of `enum` values can hold up to 100 million values, which is larger than a _small_ vector of `text` values limited to 2.75 million values. Thus, for language constructs like  `each` blocks and `autodiff` blocks, which expect to operate iteration-wise with chunks of data that fit in a page, it is recommended to use `enum` whenever possible.

As a rule of thumb, when considering a `text` column in a `read` block, if the script logic does not sort against this column, and if its cardinality (i.e. number of distinct values) is less than 10,000 distinct values then, we suggest to type this column as an anonymous enum instead. <!-- TODO: what's an anonymous enum ? -->

Beyond 10,000 distinct values, there might be a gain of performance when converting a `text` column into an `enum`, but a loss of performance may also happen due to the cost involved in creating the underlying dictionary.
