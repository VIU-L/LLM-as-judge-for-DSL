+++
title = "User defined functions"
description = "User defined functions are, as the name suggests, functions that are defined within an Envision script rather than being part of the standard library of functions."
weight = 6
+++

User defined functions are, as the name suggests, functions that are defined within an Envision script rather than being part of the standard library of functions. In this section, for the sake of brevity, functions refer to “user defined functions”.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Purpose

Functions allow you to **factorize logic**, that is, to avoid writing the same logic in many different places, and replacing those occurrences by calls to the same functions.

Functions offer **loop-like behaviors** and represent a class of alternatives to, well, actual loops. Unlike loops, functions - as introduced by Envision - offer better guarantees for both correctness and performance.

There are two flavors of functions respectively identified by the keywords `pure` and `process`. Processes (i.e `process` functions) are more complex than pure functions. Also, processes are intended to be instrumented through the `by`, `at`, `sort`, `scan` options that we have previously covered while introducing the aggregators. It turns out that aggregators are a specialized class of processes.

Neither pure functions nor processes have any _side effects_ on their arguments or options. In this regard, Envision is a strictly _functional_ language (as in _mathematical functions_), and the same goes for functions, even those that are defined by users.

Processes, however, do maintain an _internal state_ (or simply _state_) that changes through their lifecycle. Intuitively, the state represents the information that is maintained while the computation is in progress. For example, for a _sum_, the partial sum associated with the numbers added so far is the state.

_Advanced remarks_: The way Envision approaches functions is probably somewhat surprising to most experienced programmers. In mainstream programming languages, compute and memory usage are (largely) delegated to the programmer. Depending on the language, more or less, tooling is baked into the language to ease this management (e.g. a garbage collector) but nonetheless the programmer is expected to be the one in charge of the computational resources. Envision approaches the problem from a different perspective where the functions that compile automatically benefit from desirable properties in regards to the computational resources. Supply chain scientists are not expected to be intimately familiar with those. The underlying platform ensures that the amount of resources consumed remain roughly proportional to the amount of data while leveraging data parallelism to the greatest extent, to keep wall-clock time under control even when processing terabytes of data.

## Pure functions

Functions take a series of arguments, do some processing and return a series of values. All functions are declared with the keyword `def`. Pure functions, specified with the keyword `pure`, are the simplest kind of function. Let’s illustrate how a simple `hello()` function that prefixes `Hello` to a text value passed as an argument can be defined:

```envision
def pure hello(a : text) with
  return "Hello \{a}"

greeting = hello("World!")

show label greeting
```

Which, unsurprisingly, displays `Hello World!`.

The first line of the above script contains the declaration of the `hello()` function. This declaration starts with the keyword `def` and ends with the keyword `with`. The keyword `pure` indicates the type of the function. The argument is named `a`, and its data type is specified through the colon (`:`) symbol. As usual, `with` opens a new block, and thus the next line comes with an extra level of indentation. Then, the second and last line of the function definition uses the keyword `return` to specify the value returned by the function. The function `hello()` is then called to define the scalar value `greeting`, and this value is finally displayed through a `label` tile at the last line of the script.

All the function’s declarations require the sequence of keywords `def`, `with` and `return`. Also, the last statement of the function block must be a `return` statement. The type of the function can be either `pure` or `process` - we will be getting back to the latter in the following. Finally, a function must be declared before being called. The call syntax is identical to the one used to call functions from the standard library.

Functions (processes included) come with table-free (i.e. scalar) arguments and return a tuple of table-free values as well. The compiler does not allow the use of a table prefix within the function declaration line or within the function body. This design differs from regular Envision expressions that always have an affinity to a specific table, even if it’s only the `Scalar` table. While the terminology can be a bit confusing, when we say that functions are _scalar_, we indicate they operate over values instead of vectors.

The scalar nature of functions offers the possibility to automatically vectorize them, i.e. let them take a vector as input and return a vector as output as illustrated by:

```envision
table Audience = with
  [|as Folks |]
  [| "Ladies" |]
  [| "Gentlemen" |]
  [| "Mr. the President" |]

def pure hello(a : text) with
  return "Hello \{a}"

show table "Greetings" with
  hello(Audience.Folks) as "Hello!"
```

Which displays the following table:

| Hello!                 |
|------------------------|
| Hello Ladies           |
| Hello Gentlemen        |
| Hello Mr the President |

In the above script, the function `hello()` is being implicitly called three times, once for every line of the `Audience` table.

Under the hood, the Lokad platform not only vectorizes the `hello()` function, the platform can also distribute the computation over multiple CPUs and even multiple machines if the workload justifies such a high degree of parallelism (i.e. large vectors passed as argument).

### Arguments and return values

Functions can have multiple comma-separated arguments as illustrated by:

```envision
def pure myProduct(a : number, b : number) with
  p = a * b
  return p

r = myProduct(6, 7)

show label "\{r}"
```

In the above script, the variable `p` is introduced as a local variable.

Functions can also return multiple values through tuples as illustrated by:

```envision
def pure euclidianDiv(a : number, b : number) with
  quotient = floor(a / b)
  remainder = a - quotient * b
  return (quotient, remainder)

q, r = euclidianDiv(43, 6)

show label "\{q}, \{r}"
```

The syntax to deconstruct the returned tuples is identical to the one introduced previously for `with` blocks (cf. the previous section “Scoping and tuples”).

While defining a function, it is possible to call other functions as long as they are either part of the standard library (as illustrated by calling the function `floor()` above) or that they have been defined before. However, while processes can call both pure functions and processes, pure functions can only call pure functions. We will revisit this angle in greater detail in the following.

### Branching

A branch refers to an instruction that tells the computer to execute a different part of a program rather than executing statements one by one. Branches are supported by functions through the keywords `if .. else if .. else ..`. Let’s consider a function that provides a visual indicator that a measurement is growing with:

```envision
def pure isGrowing(oldValue : number, newValue : number) with
  r = ""
  if oldValue < newValue
    r = "yes"
  else if abs(oldValue - newValue) < 0.01
    r = "maybe"
  else
    r = "no"
  return r
```

In the above script, the `if` keyword is used to branch the flow of execution within the function. The variable `r` is defined with the empty text value.  If the expression `oldValue < newValue` is evaluated as `true` then `r` is overwritten with the text value `yes`. If not, then another test is made, if `oldValue` is close to `newValue` then, `r` is overwritten with the `maybe` text value. Finally, if both previous conditions were wrong, then `r` is overwritten with the value `no`.

The three statements`if`, `else if` and `else` introduce blocks, hence, in the line that follows any of those statements, an extra level of indentation must be used. Also, `else if` and `else` statements are both optional. For example, the script above can be rewritten in a slightly more concise form by taking advantage of this:

```envision
def pure isGrowing(oldValue : number, newValue : number) with
  r = "no"
  if oldValue < newValue
    r = "yes"
  else if abs(oldValue - newValue) < 0.01
    r = "maybe"
  return r
```

The above script is logically strictly equivalent to the previous one. However, the `else` statement is omitted as the `r` variable is already initially defined with the text value `no`.

Along with branching, early termination is also supported. Functions can be declared with multiple `return` statements. The following script illustrates how the previous example can be further simplified:

```envision
def pure isGrowing(oldValue : number, newValue : number) with
  if oldValue < newValue
    return "yes"
  else if abs(oldValue - newValue) < 0.01
    return "maybe"
  return "no"
```

The above script is logically equivalent to the two previous ones. However, we omit entirely to declare a local variable `r`, and leverage three distinct `return` statements to achieve the same behavior.

It is also possible to omit the final `return` statement if all branches do return:

```envision
def pure isGrowing(oldValue : number, newValue : number) with
  if oldValue < newValue
    return "yes"
  else if abs(oldValue - newValue) < 0.01
    return "maybe"
  else
    return "no"
```

When multiple `return` statements are found in the declaration of a function, they must all return the same data type. For example, the following function attempts to return both a number and a text, which does not compile:

```envision
def pure myAbs(a : number) with
  if a > 0
    return a
  return "negative" // WRONG! Incompatible returned type Number against Text
```

### Overloading

It is possible to declare multiple functions that have the same name, a mechanism known as _overloading_ as long as they don’t have the same argument types. For example the following script declares to `myAdd()` functions:

```envision
def pure myAdd(a : number, b : number) with
  return a + b

def pure myAdd(a : text, b : text) with
  return "\{a}\{b}"
```

It is not allowed to overload the names of the standard library function.

### Context capture

Functions operate quasi-independently from their context. However, constants - defined outside the function declaration block - can contribute to the logic of the function. The following script illustrates this mechanism:

```envision
const a = 42

def pure myAdd(x : number) with
  return x + a

show scalar "" with myAdd(13) // 55
```

In the above script, the variable `a` is first declared as a constant. The variable `a` is then used in the declaration of the function `myAdd`. We say that the variable `a` is _captured_ by the function `myAdd`.

**Roadmap**: the `with` block can be seen as an anonymous function where all the arguments are implicitly defined through captured variables. We plan to allow access to non-constant captured variables at some point.

### Limitations

While it is authorized to have a function calling either a previously defined function or a function of the standard library, functions cannot call themselves recursively.

```envision
def pure factorial(a : number) with
  if a <= 1
    return 1
  return a * factorial(a - 1) // WRONG! recursive call not allowed
```

## Processes

While functions are _scalar_ in design, they are intended to be ultimately used on vectors. This usage pattern implies that while a single function call is written (in the script), the underlying function actually gets called multiple times, once per table line. So far, with pure functions, those calls were kept strictly decoupled. The whole point of processes is to introduce coupling between the calls in order to perform calculations that would have otherwise been impossible under the strict decoupling rule. Let’s revisit our greeting examples with:

```envision
table Audience = with
  [|as Folks |]
  [| "Ladies" |]
  [| "Gentlemen" |]
  [| "Mr. the President" |]

def process hello(a : text) with
  keep call = 0
  call = call + 1
  return ("Hello \{a}", call)

Audience.Hello, Audience.Call =
  hello(Audience.Folks) scan Audience.Folks

show table "Greetings" with
  Audience.Hello
  Audience.Call
```

Which displays the following table:

| Name                   | Call |
|------------------------|------|
| Hello Ladies           | 2    |
| Hello Gentlemen        | 1    |
| Hello Mr the President | 3    |

In the above script, `hello()` is declared as a process function - or simply process - through the use of the `process` keyword (which replaces the `pure` keyword that we have used so far). Then, the variable `call` is introduced and initialized with the `0` value by the keyword `keep`, which indicates that this variable is part of the _state_ of the process. This state is preserved from one execution of the process to the next. At each execution, the variable `call` is incremented through the line `call = call + 1`. Finally, at each execution, a tuple containing both the greeting and the call index is returned.

The `scan` option, as detailed earlier in the “Aggregating” section, entails a sorting behavior. Thus, the `Audience` table gets sorted against `Audience.Folks` and then, the process `hello()` is repeatedly executed for each line of the table.

A process maintains an internal scalar _state_ that is preserved across the calls. A process is a function, but not a _pure_ function, because a side effect is involved: the state of the process gets modified by each successive call. Nevertheless, there are no side effects as far as arguments or options are concerned.

A process’s calls involve (call) options such as `by`, `at`, `sort`, `scan` that we already introduced in the “Aggregating” section. These options specify the fine print of the sequence of calls (executions) to be used for the process. In fact, most of the aggregators can almost be re-implemented with processes as illustrated by `mySum()` and `myAvg()` in:

```envision
table Numbers = with
  [| as N |]
  [| 3 |]
  [| 4 |]
  [| 8 |]

def process mySum(a : number) with
  keep sum = 0
  sum = sum + a
  return sum

def process myAvg(a : number) with
  return mySum(a) / mySum(1)

sum = mySum(Numbers.N) sort Numbers.N
avg = myAvg(Numbers.N) sort Numbers.N

show summary "" with sum, avg
```

Unlike some aggregators, all processes need a sort order to be specified, either via the keyword `sort` or via the keyword `scan`. Indeed, the Envision compiler is not capable of automatically detecting when ordering happens to be inconsequential, and thus, ordering is enforced to eliminate potential ambiguities. However, the `auto` keyword can be used to specify the use of the canonical order of the table itself:

```envision
def process mySum(x : number) with
  keep s = 0
  s = s + x
  return x

table T = extend.range(10)
T.S = mySum(T.N) scan auto
show table "" a1b10 with T.N, T.S
```

### Process lifecycle

The lifecycle of a process starts with its initialization, followed by a series of updates, each update includes the emission of a result, and ends with its reset. In order to walk through this lifecycle, let’s revisit a variant of the script introduced in the previous section with:

```envision
table Audience = with
  [|as Folks, as Kind |]
  [| "Ladies", "cohort" |]
  [| "Gentlemen", "cohort" |]
  [| "Mr. the President", "person" |]
  [| "Ms. the President", "person" |]

def process hello(a : text) with
  keep count = 0
  count = count + 1
  return ("Hello \{a}", count)

Audience.Hello, Audience.Count = hello(Audience.Folks)
                                 by Audience.Kind
                                 scan Audience.Folks

show table "Greetings" with
  Audience.Hello
  Audience.Count
```

Which displays the following table:

| Name                   | Call |
|------------------------|------|
| Hello Ladies           | 2    |
| Hello Gentlemen        | 1    |
| Hello Mr the President | 1    |
| Hello Ms the President | 2    |

In the above script, we add a second vector `Audience.Kind` to the `Audience` table. Then, when calling the `hello()` function we add the `by Audience.Kind` option, which wasn’t present in the previous execution of the script. As a result, we observe that in the displayed table calls are counted twice, first for the `cohort` group and second for the `person` group.

Under the hood, the lifecycle undergone by the `hello()` process is as follows:

* initialize `count` at zero
* process the `Ladies` line, and emit the result `Hello Ladies`
* process the `Gentleman` line, and emit the result `Hello Gentlemen`
* reset
* initialize `count` at zero
* process the `Mr the President` line, and emit the result `Hello Mr the President`
* proces the `Ms the President` line, and emit the result `Hello Ms the President`
* reset

The groups identified though the option `by` specify when the process must be initialized and reset. When scanning, a result is emitted for each line processed. However, when simply aggregating, the result is only emitted for the last line of the group.

As pure functions don’t have a group-level lifecycle they can’t internally call a process. However, the opposite works: a process can internally call pure functions, as well as processes.

### Group arguments

Group arguments exist for processes. We have already encountered this kind of arguments in the section “Aggregating”, and we have seen they are introduced by the semicolon (`;`) delimiter. The group arguments are aligned (table-wise), as the name suggests, with the underlying group table. Let’s illustrate this mechanism with a variant of the script introduced in the subsection “Aggregating, Group arguments”:

```envision
table Variants = with
  [| as Product, as Color, as Limit  |]
  [| "pants", "blue", " " |]
  [| "shirt", "pink", ", " |]
  [| "shirt", "white", ", " |]
  [| "socks", "green", " - " |]
  [| "socks", "yellow", " - " |]

table Products[Product] = by Variants.Product
Products.Limit = same(Variants.Limit)

def process myJoin(a : text; limit : text) with
  keep c = ""
  if c == ""
    c = a
  else
    c = "\{c}\{limit}\{a}"
  return c

Products.Colors = myJoin(Variants.Color; Products.Limit)
                  sort Variants.Color // 'by Products' is implicit

show table "Colors" with
  Product
  Products.Colors
```

Which also displays the following table:

| Product | Colors         |
|---------|----------------|
| pants   | blue           |
| shirt   | pink, white    |
| socks   | green - yellow |

The difference between the above script and its original version from the “Aggregating” section is the use of the `myJoin()` process, which re-implements the `join()` aggregator found in the standard library. While declaring the process, group arguments are introduced _after_ the semicolon delimiter. The core logic of `myJoin` uses a single text variable as its state, which gets expanded through concatenation at every execution. The first execution has to be special-cased, hence the branch `if c == ""` as the delimiter is omitted when there is only a single value.

A process can have multiple arguments separated by commas (`,`) and multiple group arguments also separated by commas. The two kinds of arguments are delimited by a semicolon (`;`). The group arguments are available all the time, but their values remain unchanged for the duration of the cycle associated with the group.

_Advanced remark_:  The native implementation of `join()` is more efficient than its naive implementation `myJoin()` as introduced above. In Envision however, text values are limited to 256 characters, hence, even the naive implementation would be limited, by design, in its capacity to deliver bad performance.

### Defaults on empty groups

Processes do return values even on empty groups. Envision provides several mechanisms to control those values. The following script provides side-by-side alternatives, clarifying the behavior of the process over an empty group.

```envision
def process myProductNoDefault(x : number) with
  keep prod = 4 // not set on empty groups
  prod = prod * x
  return prod

def process myProduct(x : number) default 1 with
  keep prod = 4 // not set on empty groups
  prod = prod * x
  return prod

table T = extend.range(5)

keep where (T.N > 10)

x = myProductNoDefault(T.N) sort T.N   // 0
y = myProduct(T.N) sort T.N            // 1
z = myProduct(T.N) sort T.N default 42 // 42

show summary "" a1c1 with x, y, z
```

In the above script, the `keep where` statement ensures that the table `T` is empty until the end of the script. Thus, the process calls which define `x`, `y` and `z` are performed over an empty table:

* `x` illustrates the usual behavior where the process falls back on the default value for the returned data type.
* `y` illustrates a process which explicitely states its own default value. Indeed, the process `myProduct()` is declared with `default 1` prior to the `with` keyword, overridding the implicit `default 0`.
* `z` illustrates an explicit override of the process definition by specifying `default 42` on the calling site.

<!-- Lack of tuple support https://lokad.atlassian.net/browse/LK-8433
when declaring the default in the process definition. -->

### State initialization

The state of a process includes all its _state variables_, i.e. variables that are declared with the keyword `keep`.  Let’s illustrate the capabilities of the state initialization with:

```envision
table Numbers = with
  [| as N |]
  [| 3 |]
  [| 4 |]
  [| 8 |]

def process mySum(a : number; init : number) with
  keep cpy = init
  keep sum = init + abs(-1)
  sum = sum + a
  return sum

sum = mySum(Numbers.N; 1000) sort Numbers.N

show summary "" with sum
```

Which displays the result 1016.

The state variable `cpy` is initialized with the group argument `init`. Then, in turn, the state variable `sum`  is initialized using the other state variable `init` along with an expression `abs(-1)` that evaluates to `1`. The process is called with `1000` as the sole `init` value as there is only one group in this case and returns 1016, which gets displayed.

State initialization has to follow several rules. All the `keep` statements must be grouped at the top of the function declaration prior to any alternative statement. The state variable, i.e. defined with `keep`, can use any group argument in its defining expression, as well as any other state variable that has already been defined. The definition expression can use pure functions, either user defined or from the standard library.

### Process instances

A process is the combination of a state and transitions (between states). The syntax introduced so far blends the state and its transition in a fairly concise manner, however there are situations where it is useful to de-entangle the two. A **process instance** is a construct offered by Envision to perform this disentanglement. Let’s illustrate how a process instance is introduced within a process with:

```envision
table Numbers = with
  [| as N |]
  [| 2 |]
  [| 4 |]
  [| 8 |]

def process mySum(a : number) with
  keep process myInstance = sum(number)
  statePlusOne = myInstance + 1
  updatedState = myInstance(a)
  return (statePlusOne, updatedState)

Numbers.StatePlusOne, Numbers.UpdatedState = mySum(Numbers.N)
                                             scan Numbers.N

show table "" with Numbers.StatePlusOne, Numbers.UpdatedState
```

Which displays the following table:

| StatePlusOne | UpdatedState |
|--------------|--------------|
| 1            | 2            |
| 3            | 6            |
| 7            | 14           |

The above script introduces a process instance named `myInstance` with the syntax `keep process`. On the left side of the assignment, the first keyword `keep` indicates that the statement belongs to the realm of the process state; then, the second keyword `process` indicates that a process instance is about to be defined. On the right side of the assignment a function (either pure or process) is identified by its signature.

The process instance `myInstance` has a dual purpose. First, it can be used to access the state of the process as done in the next line `statePlusOne = myInstance + 1`. Second, it can be used to update the process instance as done in the line that follows `updatedState = myInstance(a)`.

The syntax to define a process instance follows the pattern `fname(type1, type2, type3)`, which starts with the function name, followed with the list of types accepted by the function. This design allows you to pick the right function, even in the presence of multiple overloads. When group arguments are present the syntax becomes `fname(type1, type2, type3; arg1, arg2)`, which introduces the usual semicolon `;` separator followed by the actual group argument values.

The following script illustrates the process instance syntax in presence of group arguments:

```envision
table Variants = with
  [| as Product, as Color, as Limit  |]
  [| "shirt", "pink", ", " |]
  [| "shirt", "white", ", " |]
  [| "socks", "green", " - " |]
  [| "socks", "yellow", " - " |]

table Products[Product] = by Variants.Product
Products.Limit = same(Variants.Limit)

def process myJoin(a : text; limit : text) with
  keep process myInstance = join(text; limit)
  return (myInstance, myInstance(a))

Variants.State, Variants.Updated =
                  myJoin(Variants.Color; Products.Limit)
                  by Variants.Product
                  scan Variants.Color

show table "Colors" with
  Product
  Variants.State
  Variants.Updated
```

Which displays the following table:

| Product | State | Updated        |
|---------|-------|----------------|
| shirt   |       | pink           |
| shirt   | pink  | pink, white    |
| socks   |       | green          |
| socks   | green | green - yellow |

In the above script, the process instance is defined with `join(text; limit)`, which mixes a data type `text` followed by an actual text value `limit`. From this point, `myInstance` behaves as if it doesn’t have a group argument anymore, as this argument has already been set. Hence, the call `myInstance(a)` is part of the return statement.

The definition of a process instance must include explicit values for the group arguments, if any. Those explicit values are subject to the same rules that govern state variables: the expression must be built from group arguments (of the very process being defined) or from previously defined state variables. When the process instance is later called to update its state, group arguments are omitted.

Finally, process instances can also be used when tuples are returned, as illustrated by the following script:

```envision
table Numbers = with
  [| as N |]
  [| 2 |]
  [| 4 |]
  [| 8 |]

def process MinMax(a : number) with
  keep min = +1000000
  keep max = -1000000
  if a < min
    min = a
  if a > max
    max = a
  return (min, max)

def process MinMax2(a : number) with
  keep process myInstance = MinMax(number)
  min, max = myInstance(a)
  return (min, max)

Numbers.Min, Numbers.Max = MinMax2(Numbers.N) scan Numbers.N

show table "" with Numbers.N, Numbers.Min, Numbers.Max
```

Which displays the following table:

| N | Min | Max |
|---|-----|-----|
| 2 | 2   | 2   |
| 4 | 2   | 4   |
| 8 | 2   | 8   |

In the script above, the process `MinMax2()` is a simple wrapper around `MinMax()` introduced for the prime purpose of illustrating how process instances can also return tuples, as done with `min, max = myInstance(a)`.

<!--
## Special functions

TODO: sumlagged()

```envision
def process mySumLagged(quantity : number, writeOffset : number) with
  keep backing = linear(0)
  backing = shift(backing, -1)
  backing = backing + diracz(writeOffset) * quantity
  return valueAt(backing, 0)
```

TODO: calling functions from functions

 The nature of the function is pure or process
- purefunc(vector) is a map
- purefunc(scalar) is a call (e.g. in the body of another function)
- process(vector) is an aggregation (or fold, for the functionally minded)
- process(vector) scan X is a scan
- process(scalar) is a call (e.g. in the body of another process function)
- process(init) as x is an instantiation (in the body of another process function)
-->
