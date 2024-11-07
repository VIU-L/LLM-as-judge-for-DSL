+++
title= "Glossary"
weight= 1
draft= false
+++

This glossary lists key concepts that permeate Envision and its environment.

**variable**: a valid identifier that can be read or assigned.

**reserved keyword**: a word that comes with a special treatment by Envision. A variable cannot be named with a reserved keyword. Ex: `where`.

**scalar**: the simplest kind of variable that holds just one value. A scalar does not have a dot (.) in its name. Ex: `myValue`.

**type**: a value can be of several distinct types. The most notable types are number, text, boolean, date, ranvar and zedfunc.

**table**: a tabular dataset that typically includes multiple vectors. Tables are usually populated based on the content of flat files.

**vector**: a specific kind of variable that contains a vector of values (in the mathematical sense for "vector"). A vector has a dot (.) in its name. The first part, before the dot, is the table that contains the vector. Ex: `Products.Color`.

**page**: a segment of values within a vector. Large vectors may require multiple pages. The option `small` ensures that vectors of a given table do not spread over multiple pages. Certain capabilities of Envision only work with single-page tables, i.e. small tables. The maximal page size depends on the type of the vector.

**function**: a named set of operations leveraging data passed as argument(s). Functions have no side-effects. Functions can be built-in or user-defined.

**process**: a type of function that can be applied to an array of values to produce either cumulative values (an aggregation) or a final value (scan).  Most aggregators and accumulators are _processes_. Ex: `sum( .. )`

**call option**: a small set of standardized options to alter the behavior of a process, for example by imposing a specific grouping or a sorting order. Ex: `first( .. ) sort ..`

**indentation**: the number of whitespace characters at the beginning of each code line. Envision has significant whitespace. A block begins when indentation level increases, and ends when the indentation level decreases.

**statement**: a stand-alone piece of code that usually fits on a single line. The two most notable statements are assignments and filters.

**block**: a series of statements and blocks that all have the same indentation level. Blocks are introduced by specific statements, such as filters or processes declaration.

**assignment**: a statement that assigns a new value to a variable using the symbol `=`, creating it if it does not exist.

**filter**: a kind of statement that restricts the data that exists in the block that follows the filter statement, typically using the reserved keyword `where`. Filters can be nested.

**schema**: A _named schema_ specifies the content of a table (column names and types). Schemas are intended to stabilize and document the format of the tabular files either written or read by Envision scripts. A _path schema_ also specifies the placement of the files.

**downstream / upstream**: If table T is upstream of U, then for each line of U, there is one and only one line associated in T, thus both `U.X = T.X` (broadcasting T in U) and `T.X = aggregator(U.X)` (aggregating U in T) are legit. If table T is upstream of U, then table U is downstream of T.

**read statement**: a kind of statement that defines how data is loaded from files into tables.

**show statement**: a kind of statement that defines a tile to be rendered in the resulting dashboard.

**tile**: a construct that takes vectors as input and produce a visual block in the dashboard (ex: a linechart).

**def statement**: a kind of statement introducing a user-defined function.

**script**: a valid piece of Envision code.

**project**: the named container for a script.

**run**: the execution of a project and its resulting dashboard.

**script editor**: the UI that let users modify their Envision scripts.

**tile editor**: the WYSIWYG editor that lets users rearrange their tiles and the color of their tiles.

**variadic**:  a function is said to be variadic if it accepts a varying number of arguments. By convention, it's the last argument that can be repeated.
