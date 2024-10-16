+++
title = "Modules"
description = ""
weight = 9
+++

Modules are introduced in Envision in order to share logic between scripts and allow some degree of code reuse. A module is a block of Envision code, however, unlike a script, a module cannot be executed, only imported piecewise in a script and then executed. From a module, it’s possible to _export_ elements of logic. From a script, it’s possible to _import_ those elements.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Overview

Let’s create a module named `sample/my-module` from the `Projects` view by clicking the dropdown next to `Create Envision script`. Through the code editor, let’s enter the follow code for the module itself, and click `Save`:

```envision
// Module named 'sample/my-module'
export const myHello = "Hello"
export const myWorld =  "World!"
```

The above module exports two scalar text constants. As the name suggests, the keyword `export` identifies the values found within the module and makes them accessible outside the external scripts.

<!--  TODO: screenshot of the module code editor -->
Unlike a script, a module cannot be executed and consequently does not produce dashboards. While editing the code of the module, the code editor does not offer the button `Start Run` as part of the right sidebar, as is usually the case when editing scripts.

A script can then be introduced:

```envision
import "sample/my-module" as M with
  myHello
  myWorld

show scalar "" with "\{myHello} \{myWorld}"
```

In the above script, the module is loaded with the keyword `import` followed by the pathname of the module itself. The keyword `with` introduces a block, intended, that contains the list of elements found in the module to be imported in this script.

All the variables found in the module don’t have to be exported. The following module illustrates how constants can be combined, exporting only the result:

```envision
// Module named 'sample/my-module'
const t1 = "He"
const t2 = "llo"
export const myHello = "\{t1}\{t2}"
export const myWorld =  "World!"
```

In the above module, the variables `t1` and `t2` are not exported. Thus, it is not possible for a script to import either `t1` or `t2`. Only the variables `myHello` and `myWorld` are eligible for import as they are marked with `export` in the first place.

The Envision syntax for modules is mostly a subset of the Envision syntax for scripts. Most notably `read` and `show` statements are not allowed in modules.

### Inline documentation

Within a module, all elements marked with `export` can be prefixed with a special triple-slash `///` comment.

```envision
// Module named 'sample/my-module'

/// This line is exported as the inline doc of 'myHello'.
export const myHello = "Hello"

/// Those two lines are exported as 
/// the inline doc of 'myWorld'.
export const myWorld =  "World!"
```

The code editor propagates this documentation to the scripts that import the module. Script-side, the inline documentation of the module becomes visible when hovering over the imported elements.

## Export scalar values

Let’s revisit the export/import of scalar values. The following script gives a more extensive illustration of the data types that can be exported.

```envision
// Module named 'sample/my-module'
export const myText = "Hello World!"
export const myNumber =  42
export const myDate = date(2021, 8, 31)
export const myBoolean = true
export const myMarkdown = """Hello World!"""
```

In turn, those values can be imported in a script:

```envision
import "sample/my-module" as M with
  myText
  myNumber
  myDate
  myBoolean
  myMarkdown

show summary "" a1b2 with myText, myNumber, myDate, myBoolean
show markdown "" a3 with myMarkdown
```

In the above script, the imported values are strongly typed based on the data types found in the module. However, it is possible to re-specify the types (for the sake of clarity) in the script as illustrated with:

```envision
import "sample/my-module" as MyModule with
  myText : text
  myNumber : number
  myDate : date
  myBoolean : boolean
  myMarkdown : markdown

show summary "" a1b2 with myText, myNumber, myDate, myBoolean
show markdown "" a3 with myMarkdown
```

Fat data types like `ranvar` or `zedfunc` cannot be exported.

## Module namespaces

The module name acts as a namespace to access its exported elements. Let’s illustrate this mechanism by revising the script that consumes the module introduced in the previous section:

```envision
import "sample/my-module" as M

show summary "" a1b2 with M.myText, M.myNumber, M.myDate, M.myBoolean
show markdown "" a3 with M.myMarkdown
```

In the above script, the module is imported and named as `M`. The exported constants are accessed by adding `M` as a prefix, as it is done in `M.myNumber` for example.

This namespacing mechanism is useful when an element of the module is only used infrequently in the script. In this case, using the prefix makes the overall script a bit more concise. This mechanism is also useful when the name of the exported variable collides with either a pre-existing variable name in the script or in another imported module.

## Chained module imports

A module can be imported by another module. This capability can be of interest to neatly organize elements that would be too numerous to conveniently fit in a single module. For example, let’s create a second module named `sample/my-module-2` with:

```envision
import "sample/my-module" as M // Module named 'sample/my-module-2'
export const myNumber =  13 + M.myNumber
```

In the above module, the module created in the first section above is imported as `M`. This module contributes to the definition of a constant `myNumber` through the reference to `M.myNumber`. The two modules have both an exported variable named `myNumber`.

The following script illustrates how to consume these two modules:

```envision
import "sample/my-module" as M1
import "sample/my-module-2" as M2

show summary "" a1b1 with M1.myNumber, M2.myNumber
```

In the above script, the two modules are respectively named `M1` and `M2`. These two names are used as a prefix to differentiate the two exported constants, which happen to both be named `myNumber` in each module.

Circular dependencies are not allowed by Envision: it is not possible to have modules cross-importing themselves.

## Export user-defined functions

User-defined functions can be exported in modules, as illustrated by the following module:

```envision
// Module named 'sample/my-module'
export def pure plusOne(x: number) with
  return x + 1
```

In the above module, the function `plusOne` is exported by prefixing its declaration with the keyword `export`. This function can then be called in script with:

```envision
import "sample/my-module" as M

show scalar "" with M.plusOne(42)
```

In the above script, the function `M.plusOne` refers to the function `plusOne` found in the module `M`. It is also possible to remove the need for the module prefix, as illustrated by:

```envision
import "sample/my-module" as M with
  plusOne

show scalar "" with plusOne(42)
```

## Export inline enums

Inline enums can be exported as illustrated by:

```envision
// Module named 'sample/my-module'
export table enum T = "A", "B"
```

In the above module, the `export` keyword is used to indicate that the enum `T` is exported. This enum can then be used in a script:

```envision
import "sample/my-module" as M with
  T

a = enum<<T>>("A")
show scalar "" with text(a)
```

Unlike the exportable elements seen so far, an `enum` has to be explicitly imported and cannot be referenced by prefixing the name of the module.

## Export table comprehensions

Table comprehensions can be exported as illustrated by:

```envision
// Module named 'sample/my-module'
export table T = with
  [| as A, as B  |]
  [| 1,    true  |]
  [| 2,    false |]
  [| 4,    true  |]
```

In the above module, the `export` keyword is used to indicate that the table `T` is exported. This table can then be used in a script:

```envision
import "sample/my-module" as M with
  T

show table "" a1b3 with T.A, T.B
```

Exported tables behave like exported enums. The table needs to be explicitly imported and cannot be referenced by prefixing the name of the module.

## Usage guidelines

As far as modules are concerned, we suggest:

* Keep module paths plain. Avoid whitespaces, capitalization and non-alphanumeric characters.
* Use folders to isolate modules from scripts. Keep modules together.
* Isolate StyleCode elements in modules to maintain a visual unity over many dashboards.
* Isolate constants such as default lead times, default margins, … in modules.
* Take advantage of the `///` structured documentation for exported elements. Don't hesitate to use long insightful comments spanning over multiple lines.
* Polish more extensively, .e.g. more documentation efforts, frequently reimported modules than stand-alone scripts.
