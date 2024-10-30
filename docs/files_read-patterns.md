+++
title = "Read patterns"
description = ""
weight = 3
+++

While the approach _1 table, 1 file_ works for small tables, say less than a million lines, it rapidly becomes impractical for larger tables, as the daily data refresh ends up requiring you to move impractically large amounts of data around. In those situations, it becomes necessary to split a table into multiple files, typically following some kind of incremental split of the data. In order to support this practice, Envision offers the _file patterns_ mechanism to consolidate many files into a single file.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Wildcard patterns

Let’s start by generating 3 files that we intend to consolidate later on:

```envision
table Products = with
  [| as Product, as Price |]
  [| "shirt", 10.50 |]
  [| "pants", 15.00 |]
  [| "hat", 5.25 |]

schema Products with
  Product : text
  Price : number

where Products.Product == "shirt"
  write Products as "/sample/products-1.csv" with
    schema Products

where Products.Product == "pants"
  write Products as "/sample/products-2.csv" with
    schema Products

where Products.Product == "hat"
  write Products as "/sample/products-3.csv" with
    schema Products
```

Each file has the same format (i.e. same columns), and the file names are essentially similar, only diverging by a suffix inserted just prior to the file extension. These files can be read in a single statement as illustrated by:

```envision
read "/sample/products-*.csv" as Products with
  Product : text
  Price : number

show table "Products" a1b3 with
  Products.Product
  Products.Price
```

Which results in the following display:

| Product | Price |
|---------|-------|
| shirt   | 10.5  |
| pants   | 15    |
| hat     | 5.3   |

In the above script, the wildcard `*`(star) character is used to capture any of the three filename variants, which ends up consolidated in a single `Products` table.

The wildcard `*` matches any character as long as it’s not a `/`, which was used to separate folders. The file pattern can also include multiple wildcards. This behavior is heavily inspired from the behavior of the `ls` command line in Linux and the `dir` command line in Windows.

A single script can contain multiple `read` statements. The ordering of those `read` statements has no impact on the set of files captured by each statement. In fact, the ordering of the `read` statements has almost no impact whatsoever. There is a single exception to this principle of unordered `read` statements with column inferences (see next section).

If a file is captured multiple times through multiple `read` statements, the content of the file is loaded multiple times.

## Pattern unions

Heterogeneous sets of files that cannot be captured by a single file pattern, or that do not follow the same format, can still be consolidated in a single table through multiple `read` statements. The consolidation is achieved through a mechanism referred to as _pattern unions_.

<!-- [vermorel] 2020-07 TODO: We intend to disallow redundant read columns. See https://lokad.atlassian.net/browse/LK-6590 -->

Let’s leverage the file created in the previous section to illustrate how the `Products` table can be read from two distinct `read` statements:

```envision
read "/sample/products-1.csv" as Products with
  Product : text
  Price : number

read "/sample/products-*.csv" as Products with
  Product : text
  Price : number

show table "Products" a1b3 with
  Products.Product
  Products.Price
```

Which results in the following display:

| Product | Price |
|---------|-------|
| shirt   | 10.5  |
| shirt   | 10.5  |
| pants   | 15    |
| hat     | 5.3   |

In the above script, the table `Products` appears _twice_ and, as a result, Envision ends up consolidating all the data originating from the two sets of files into a single table. The file `products-1.csv` is read twice.

However, as all the files follow the exact same format, the declaration of the column in the second `read` statement is redundant, and merely mirrors the content of the first `read` statement. Envision offers a mechanism to avoid this redundancy altogether:

```envision
read "/sample/products-1.csv" as Products with
  Product : text
  Price : number

read "/sample/products-*.csv" as Products

show table "Products" a1b3 with
  Products.Product
  Products.Price
```

This script above is strictly equivalent to the previous one. The second `read` statement omits entirely the columns that are inferred by Envision from the previous statement.

The inference of the colums is the exception to the general principles that `read` statements are unordered, as the statement that specifies the column must come first.

The two main use cases for resorting to pattern unions are either that files are dispersed among folders that can’t be captured at once with a single file pattern, or that there are various file formats involved. The example script provided in this section does not fall into either one of those two use cases, the sole point of this example is to illustrate the syntax. The varying format use case will be discussed in the “File Formats” section below.

_Advanced remark_: The first use case, the more general filename capture, could also have been addressed by the use of a more general pattern matching syntax such as regular expressions (regex). However, a general matching syntax presents a performance risk whenever millions of filenames have been matched against arbitrary complex rules. A guiding design principle for Envision is _predictible_ performance, and the performance of Envision has to remain fully decoupled from the overall number of files present in the account - as long as those files aren’t actually contributing to the script calculations.

## Pattern filters

When a wildcard is used, the read pattern can capture an arbitrarily large number of files. The _pattern filters_ allow you to restrict the capture to a subset of the original set. Usually, this behavior proves useful when the intent is to restrict the `read` statement to the “last” N files.

Leveraging again the three files created in the previous section, the following script only read two files out of the three:

```envision
read max 2 "/sample/products-*.csv" as Products with
  Product : text
  Price : number

show table "Products" a1b3 with
  Products.Product
  Products.Price
```

Which results in the following display:

| Product | Price |
|---------|-------|
| pants   | 15    |
| hat     | 5.3   |

The `max 2` option that follows the keyword `read` indicates that within all the files captured by the pattern, only the last two; based on lexicographic ordering, are kept.

More generally, the file pattern supports three filters `max`, `min` and `latest`. Both `min` and `max` sort files by name, while `latest` sorts files against their _last update datetime_ (most recent updates first). The integer that follows the filter can be omitted, the default value being 1.

Combined with the _single match_ behavior, the filters offer the possibility to select a _range_ of files. By capturing files in a first pattern (and typically ignoring them afterward), the initial capture acts as a negative condition on the second pattern.

<!-- https://lokad.atlassian.net/browse/LK-9859 
TODO: 'read' syntax needs refactoring, max/min/latest are haphazard -->
**Roadmap:** The pattern filters are somewhat unsatisfying because they don’t really connect to the rest of the Envision syntax. Both patterns and filters aren’t as expressive as we would like them to be, and as a result, the range selection is not a completely straightforward matter. Rather than adding more options, we will probably revisit this bit of syntax entirely in the future.

## Pattern expressions

The read statement takes a file pattern - a text argument - as input. So far, all the file patterns that we have used were text _literals_. However, there are situations where a _text expression_ is preferable. For example, the folder might be the same for many read statements, and it might be desirable to change the target folder without revisiting every single read statement in the script. The _pattern expressions_ are intended precisely for this purpose.

Let’s re-introduce a short script to generate a file:

```envision
table Products = with
  [| as Product, as Price |]
  [| "shirt", 10.50 |]
  [| "pants", 15.00 |]
  [| "hat", 5.25 |]

write Products as "/sample/products.csv" with
  Product = Products.Product
  Price = Products.Price
```

This file can then be read with the script below:

```envision
const myFolder = "/sample" // only compile-time constants may be used as 'read' argument

read "\{myFolder}/products.csv" as Products with
  Product : text
  Price : number

show table "Products" with
  Products.Product
  Products.Price
```

In the above script, the folder is isolated in a scalar text variable named `myFolder`. This variable is then injected in the file pattern itself through the usual text interpolation mechanism that we have seen in an earlier section.

The variables that contribute to the file patterns have to be _compile-time constants_. As a rule of thumb, in Envision any basic operation, say a text concatenation, that involves only constant arguments produces a constant result. This mechanism is known as _constant propagation_.

It is also possible to directly pass a text expression (instead of a text literal) as the file pattern, as done in the following script:

```envision
const myFolder = "/sample"
const myPath = "\{myFolder}/products.csv" // compile-time constant

read (myPath) as Products with
  Product : text
  Price : number

show table "Products" with
  Products.Product
  Products.Price
```

Due to parsing and considering the design of Envision itself, unless it’s a text literal, the text expression of the file pattern has to be surrounded by parentheses `(` and `)`.

**Roadmap**: The file count integer associated with the `max`, `min` and `latest` option has to be a number literal. It does not benefit from any constant propagation mechanism. However, it’s unlikely that this feature will be introduced later on as such. Such a capability is more likely to emerge from the larger decoupling overhaul of the read statements (decoupling patterns from formats).
