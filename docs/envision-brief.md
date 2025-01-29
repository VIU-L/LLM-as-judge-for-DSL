Use the documentation below to answer the Envision question.

# Envision, a DSL for predictive analytics

Envision is a DSL developed by Lokad for analytics and predictive optimization over business relational data, typically for supply chain purposes. Envision features array programming. It is strong-typed, imperative, functional, auto-distributed with a syntax reminiscent of Python and SQL.

An Envision script reads flat files (tables) as input from the Lokad filesystem, and produces a web dashboard as output. The web dashboard is made of _tiles_, the basic Envision construct to compose a dashboard. The output may also include flat files written to the Lokad filesystem.

Beware, Envision is indentation sensitive, like Python.
When entering a block (after `with`), the indentation increases by two whitespaces `  `.
When dedenting of two whitespaces `  `, the block is exited.

## Data types

The build-in value types of Envision are `boolean`, `number` (float32), `text`(like nvarchar(256)), `date` (no time of day), `ranvar` (1D probability distribution, Z->R, mass 1), `zedfunc` (1D function, Z->R).

```envision
// Booleans
b = true or false // `true`, operators: and or not
b = /* inline comment */ not b // `false`
b = 5 > 2 // `true`, operators: < > <= >= == !=

// Numbers
x = 1 + 2 * 3 // `7`, operators: + - * /
x = 5 mod 2 // `1`

// Texts
m = concat("a", "b", "c") // `abc`, variadic
m = text(123) // `text` function converts most types to text
m = text(true)
m = "X = \{x} and B = \{b}" // text interpolation via \{..}
n = strlen("abc") // 3

// Dates
d = date(2023, 9, 30) // `2023-09-30`
d = d + 1 // `2023-10-01`, add 1 day
d = d - 1 // `2023-09-31`, subtract 1 day
n = d - date(2023, 9, 29) // difference in days

// Ranvars
r = poisson(1) // Poisson, lambda = 1
r = r + poisson(1) // Poisson, lambda = 1

// Zedfuncs
f = linear(1) // f(x) = x
f = f + 1 + linear(f) // f(x) = 2x + 1
```

Beware, text literals use double-quote: `"hello"`.
Path literals, only used for schemas, use single-quotes: `'myfile.csv'`.
Do not attempt to use single-quote anywhere BUT in path schemas.

## Your first script

Every script must display at least _one_ dashboard _tile_. The following script illustrates how to generate a dashboard that contains a single tile displaying _Hello World!_.

```envision
greeting = "Hello World!" 
show label greeting
```

All the statements that start with the keyword `show` indicate that a _tile_ will be displayed. Tiles are the display mechanism provided by Envision. All the tiles present in a script are consolidated in a _dashboard_.

Attention that if we use "show label", the format should be 
```envision
show label labelContent
```
without writing "with" and the label does not have a title. this is different from show table : 
```envision
show table "ChartName" with tableContent
```

The value `"Hello World!"` is called a **text literal**, a value that appears verbatim in the code. The operator `=` is the **assignment operator**.

## Tables

Envision adopts array programming, processing whole columns at once, like SQL.
The `.` operator is used to specify the table, i.e. `MyTable.MyField`.

```envision
// `sku`  is the primary dimension of `Orders` (optional)
table Orders[sku] = with
  [| as sku, as Date          , as Qty, as Price , as Category |] // headers
  [| "a",    date(2020, 1, 17), 5     , 1.5      , "cat1"      |]
  [| "b",    date(2020, 2, 5) , 3     , 7.0      , "cat1"      |]
  [| "c",    date(2020, 2, 7) , 1     , 2.0      , "cat2"      |]
  [| "d",    date(2020, 2, 15), 7     , 5.7      , "cat2"      |]
 
// `Orders.Amount` is the vector `Amount` within `Orders`
Orders.Amount = Orders.Qty * Orders.Price // implicit loop, all lines at once

// `show` introduces a tile of type `table`. `a1b3` is the position of tile (like Excel cells A1 to B3).
show table "Total Sales by SKU" a1b3 with
  // `with` introduces a block (like `:` in Python), followed by extra indent.
  Orders.Category                              // 1st column, header `Category` (autogen)
  count(Orders.*) as "SKUs"                    // 2nd column, header `SKUs` (via `as`)
  sum(Orders.Amount) as "Amount" { unit:"$" }  // 3rd column, format via StyleCode `{..}`
  // `group by` only allowed with a `show` block (optional)
  group by Orders.Category
```

Specifying the primary dimension is optional.
Dimensions are lowercased by convention (not a requirement).

`count` and `sum` are aggregators.

Usually, tables are read from flat files:

```envision
// `expect [date]` means that `date` is a secondary dimension of `Orders`
// `Date[date]` is an auto-generated table. It spans the entire range of observed dates.
read "/sample/orders.csv" as Orders expect [date] with
  Date : date
  Quantity : number
 
show linechart "Daily Quantities" a1b4 with 
  sum(Orders.Quantity)
```

A more elaborate example:

```envision
// `id` primary dimension
read "/sample/items.tsv" as Items[id] with
  "Id" as id : text
  Name : text
  Brand : text

// `expect [date]` is the go-to-option to access to `Day[date]`, `Week[week]` and `Month[month]` tables.
read "/sample/orders.tsv.gz" as Orders expect [id, date] with
  "Id" as id : text
  "Date" as date : date
  Quantity : number
  NetAmount : number
  Currency : text
 
lastOrderDate = max(Orders.Date) // Aggregate to the `Scalar` table by default
 
// Filtered tables: `Day`, `Week`, `Month` and `Orders`
// `Orders` is filtered too because it has `date` as secondary dimension (via `expect`).
where date >= lastOrderDate - 365 
  // The most frequently used currency during the last year
  currency = mode(Orders.Currency) when (date >= oend - 365)

  // Convert all amounts to this most frequent currency
  Orders.NetAmount = forex(Orders.NetAmount, Orders.Currency, currency, date)

  // `{ .. }` is StyleCode (a bit like CSS)
  show scalar "Turnover" d2 with 
    sum(Orders.NetAmount) { unit:#(currency) }
  show scalar "Orders lines" e2 with
    count(Orders.*)
  show scalar "Units" f2 with 
    sum(Orders.Quantity)
// De-indent, we have exited the scope of the `where` block

// Back to the global scope
show scalar "All units ever sold" d3 with
  sum(Orders.Quantity)
```

The `as` keyword is used to rename fields found in the flat file.

## Filtering tables

The `where` statement opens a new block where the table has been filtered.

```envision
table T = with
  [| as N |]
  [| 1 |] // line 1
  [| 2 |] // line 2
  [| 3 |] // line 3
table U = with
  [| as L |]
  [| "a" |] // line 1
  [| "b" |] // line 2

// Filtered tables: `T`
where T.N > 1 // lines left in `T`: 2, 3
  // Filtered tables: `U`
  where U.L != "a" // lines left in `U`: 2
    show scalar "T" a1 with count(T.*) // `2`
    show scalar "U" b1 with count(U.*) // `1`
  // end of `where U.L != "a"`
  show scalar "T" a2 with count(T.*) // `2`
  show scalar "U" b2 with count(U.*) // `2`
// end of `where T.N > 1`
show scalar "T" a3 with count(T.*) // `3`
show scalar "U" b3 with count(U.*) // `2`
```

A single `where` statement can filter more than 1 table.
When filtering a table, all its downstream tables are filtered too.

```envision
table T = with
  [| as N, as Cat |]
  [| 1, "a" |] // line 1
  [| 2, "a" |] // line 2
  [| 3, "b" |] // line 3

// `U` is a grouping table over `T`
table U[cat] = by T.Cat // `U` is now upstream of `T`, `T` is downstream of `U`.

// Filtered tables: `U`, `T`
where cat != "a" // lines left in `T`: 2, 3
  show scalar "T" a1 with count(T.*) // `1`
  show scalar "U" b1 with count(U.*) // `1`
// end of `U.Cat != "a"`
show scalar "T" a2 with count(T.*) // `3`
show scalar "U" b2 with count(U.*) // `2`
```

## Block scopes

A variable created in the scope of a block cannot be used outside its original scope.

The script below does not compile:

```envision
// Create a table with 5 lines
table T = extend.range(5) // special, auto create `T.N : number`

// `T.X` is defined for the whole table `T`
T.X = "A"

// Filtered tables: `T`
where T.N >= 4 // Filtered tables: `T`
  // entering the `where` block, +2 indent
  T.X = "B"
  T.Y = "C" // `T.Y` belong to the scope of the `where` block
// exiting the `where` block, -2 indent

// The `show` has no indent
show table "T" a1b2 with
  T.X // good
  T.Y // WRONG, fails with `Undefined variable T.Y`
```

It can be fixed with:

```envision
// Create a table with 5 lines
table T = extend.range(5) // special, auto create `T.N : number`

// `T.X` is defined for the whole table `T`
T.X = "A"

// Filtered tables: `T`
where T.N >= 4
  T.X = "B"
  T.Y = "C" // `T.Y` belong to the scope of the `where` block

  // The `show` is indented, we are still in the `where` block
  show table "T" a1b2 with
    T.X // good
    T.Y // good
```

## Calendar tables

In order to display time-series, Envision offers 3 special tables: `Day[date]`, `Week[week]` and `Month[month]`.

```envision
// `expect [date]` auto-creates tables `Day`, `Week` and `Month`
read "/sales.csv" as Sales expect [date] with
  "SalesDate" as date : date
  SalesQty : number
  SalesUsd : number

// here `max(Sales.date)` would be the same
salesEnd = max(date) 

// Filtered tables: `Day`, `Week`, `Month` and `Sales`
// Tables with `date` as a secondary dimension (aka `expect`) are filtered too.
// Thus, the tables `Week`, `Month` and `Sales` are filtered too
where date > salesEnd - 365
  Month.Qty = sum(Sales.SalesQty)
  Month.Usd = sum(Sales.SalesUsd)
  show linechart "Monthly USD (last 365 days)" a6b8 with
    // entering the `show` block, +2 indent
    Month.Qty
    Month.Usd
// dedent, exiting the `where` block
show scalar "Total sales ever" with sum(Sales.SalesUsd)
// `Day.Qty` is undefined here, as we have exited its definition scope (due to dedent).
// Idem `Month.Qty` and `Month.Usd` are also undefined here.
```

Calendar tables are auto-created by having a `read` statement with `expect [date]`.
To extend the range of `Day` into the future use `span`.

Envision includes an extensive support for calendar conversions, e.g. `date(week, dayOfWeek)`, `week(year, weekOfYear)`, and calendar operations, e.g. `monthStart()`, `monday()`. As a rule of thumb, round-trips between text values and calendar values is a strong hint that the script should be rewritten to take advantage of those built-in functions.

Envision can convert a date to a week or a month, and vice versa.

```envision
d = date(2021, 3, 21)
w = week(2021, 20)
m = month(2021, 5)

show summary "Time values" a1a3 with 
  text(d) // '2021-03-21'
  text(w) // '2021-W20'
  text(m) // '2021-05'
```

The `parseDate()` function parses `text` values  into `date` values:

```envision
d = parseDate("2021-03-21")
show scalar "Parsed date" with d // 'Mar 21, 2021'
```
The two functions `text(date)` and `parseDate()` are symmetrical

## Tiles

Running an Envision script produces a dashboard, and the dashboard is composed of tiles. Envision supports multiple tiles.

```envision
table T = extend.range(10)
T.X = random.poisson(5 into T) // 'into' broadcasts scalar '5' into table 'T'
T.G = "G\{T.N}"
 
// Horizontal bars
show barchart "My Groups" a1b8 with
  sum(T.X) // must be a number
  max(T.X) // 
  group by T.G // required for 'barchart'
```

```envision
table T = extend.range(1000)
T.X = random.poisson(5 into T)
 
 // Vertical bars
show histogram "My histogram" a1f4 with T.X
```

```envision
// Day, Week and Month, the special calendar tables are implicitely created by 'span'
// (other way: use 'read' with '[date]'  as secondary dimension)
keep span date = [date(2021, 5, 1) .. date(2021, 7, 30)] 
 
Day.X = random.poisson(5 into Day)
Week.X = sum(Day.X)
Month.X = sum(Day.X)
 
show linechart "Daily (2 lines)" a1b4 with 
  Day.X
  Day.X + 3 as "X shifted" { color: "red" } // web colors 
show linechart "Weekly" a5b6 with Week.X
show linechart "Monthly" a7b8 with Month.X
```

```envision
keep span date = [date(2021, 5, 3) .. date(2021, 7,6)]
 
def pure isTuesday(d : date) with // pure function
  return d == monday(d) + 1 // body of the function
def pure isWeekend(d: date) with
  return d >= monday(d) + 5
 
// Flat replenishments of 120 units on Tuesdays.
Day.Restock = if not(isTuesday(date)) then 0 else 120 // ternary
 
// Simulating a random demand that increases on the weekend.
Day.Demand = random.ranvar(poisson(15 into Day)) // 'into' broadcasts scalar into 'Day' table
Day.Demand = if isWeekend(date) then floor(Day.Demand * 1.2 + 5) else Day.Demand
 
// Positive cumulative sum to prevent negative stock.
def process positiveCumsum(n : number) with
  keep sum = 0 // 'keep' defines the state of the process, 'sum' is persisted across calls
  sum = max(0, sum + n)
  return sum
 
Day.Stock = positiveCumsum(Day.Restock - Day.Demand) scan date
Day.Sales = Day.Stock[-1] - Day.Stock + Day.Restock // [-1] lags the table (only for calendar tables)
 
show linechart "Stock level simulator" a1h6 { legendPosition: left ; vaxis { left { axisMax: 500 } } } with
  Day.Restock as "Daily restock" { seriesType: bar ; unit: " stock" ; color:#7e7 }
  Day.Stock as "End of day stock" { seriesType: bar ; seriesOpacity: 0.6; unit: " stock" ; color:#666 }
  Day.Sales as "Daily sales" { seriesType: line ; color: gray ; seriesStack:"stackSales" ; unit: " sold" }
  Day.Demand - Day.Sales as "Unsatisfied demand" { seriesType: area ; seriesOpacity: 0.6 ; seriesStack:"stackSales" ; unit:" sold"; color:#fa0 }
  if isWeekend(date) then 1 else 0 { seriesType: background ; seriesLegend: hidden ; seriesOpacity: 0.25 ; color: #f99 }
  group by date
```

```envision
// Markdown is both a data type and a tile type.

// Single line markdown literal
m = """Hello **World**"""
show markdown "" a1b2 with m

// Multi-line markdown literal
show markdown "" a3b6 with """
# Part A
## Subpart A.1
A list of **important** remarks.
 
* remark 1
* remark 2
* remark 3
 
## Subpart A.2
# Part B
 
Less important remarks.
"""
```

```envision
table T = with 
  [| as Product, as Country |]
  [| "Shirt", "FR" |]
  [| "Hat", "FR" |]
  [| "Shirt", "UK" |]
  [| "Shoes", "UK" |]
 
T.Sales = random.poisson(10 into T)
 
show piechart "Sales per product" a1c6 with
  sum(T.Sales)
  group by T.Product
```

```envision
// The 'scalar' tile works with most data types (but only single scalar)
show scalar "options" a1b1 {tileColor: "red" ; unit: "$" } with 123 // {..}, StyleCode

myDate = date(2022, 2, 17)
onHand = 123
onOrder = 42
unitPrice = 25
 
 // The 'summary' tile supports multiple scalar values
show summary "Key figures" a2b4 with
  "Contoso A-001" as "Product Name"
  myDate
  onHand
  onOrder
  onHand + onOrder as "Total units" 
  (onHand + onOrder) * unitPrice as "Total value" {unit: "$"}
```

```envision
table T = extend.range(50)
T.X = random.uniform(0 into T, 1) 
T.Y = random.uniform(0 into T, 1)

// Display a set of 2D points, expects exactly 2 vectors as argument.
show scatter "" a1d6 with
  T.X 
  T.Y { value { color: #[if T.X > 0.5 then "blue" else "red"] } }
```

## StyleCode

Envision features a sub-language named StyleCode, inspired by CSS, to modify the tiles look & feel.

```envision
table Products = with
 [| as Product, as Color |]
 [| "pants", "blue" |]
 [| "shirt", "pink" |]
 [| "socks", "green"|]
 
show table "My Products" a1b3 with
  Products.Product { textColor: #[Products.Color] } // curly brackets {} for StyleCode
  Products.Color
```

## Glossary

This glossary lists key concepts that permeate Envision and its environment.

**scalar**: the simplest kind of variable that holds just one value. A scalar does not have a dot (.) in its name. Ex: `myValue`.

**table**: a tabular dataset that typically includes multiple vectors. Tables are usually populated based on the content of flat files.

**vector**: a specific kind of variable that contains a vector of values (in the mathematical sense for "vector"). A vector has a dot (.) in its name. The first part, before the dot, is the table that contains the vector. Ex: `Products.Color`.

**page**: a segment of values within a vector. Large vectors may require multiple pages. The option `small` ensures that vectors of a given table do not spread over multiple pages. Certain capabilities of Envision only work with single-page tables, i.e. small tables. The maximal page size depends on the type of the vector.

**function**: a named set of operations leveraging data passed as argument(s). Functions have no side-effects. Functions can be built-in or user-defined.

**process**: a type of function that can be applied to an array of values to produce either cumulative values (an aggregation) or a final value (scan).  Most aggregators and accumulators are _processes_. Ex: `sum( .. )`

**call option**: a small set of standardized options to alter the behavior of a process, for example by imposing a specific grouping or a sorting order. Ex: `first( .. ) sort ..`

**statement**: a stand-alone piece of code that usually fits on a single line. The two most notable statements are assignments and filters.

**block**: a series of statements and blocks that all have the same indentation level. Blocks are introduced by specific statements, such as filters or processes declaration. To exit the block, just de-indent.

**filter**: a kind of statement that restricts the data that exists in the block that follows the filter statement, typically using the reserved keyword `where`. Filters can be nested.

**downstream / upstream**: If table T is upstream of U, then for each line of U, there is one and only one line associated in T, thus both `U.X = T.X` (broadcasting T in U) and `T.X = aggregator(U.X)` (aggregating U in T) are legit. If table T is upstream of U, then table U is downstream of T.

**read statement**: a kind of statement that defines how data is loaded from files into tables.

**schemas**: A _named schema_ specifies the content of a table (column names and types). Schemas are intended to stabilize and document the format of the tabular files either written or read by Envision scripts. A _path schema_ also specifies the placement of the files.

**show statement**: a kind of statement that defines a tile to be rendered in the resulting dashboard.

**tile**: a construct that takes vectors as input and produce a visual block in the dashboard (ex: a linechart).

**def statement**: a kind of statement introducing a user-defined function.

## Envision reference

**Reserved keywords:** and as at auto autodiff by const cross def default define delete desc draw each else enum expect export fail false for foreach group if import in index into keep loop match mod montecarlo not or order over params read return sample scan show sort span table then true unsafe until when where while with write

**Contextual keywords:** assert barchart boolean chart date form histogram interval label latest linechart logo max min markdown month nosort number partitioned piechart plot private process pure ranvar scatter scalar single slicepicker slicetree small summary text upload week whichever zedfunc

The **operators** by increasing order of precedence:

* ..
* if then else
* (unary) + - ~ not
* ^
* (binary) * / /. mod
* + -
* (comparisons) < > <= >= == != ~~ !~ in
* and
* or
* into
* ...
* .

### Aggregators and Functions Available

* **Basic:** argmax argmin argwhichever aresame count distinct distinctapprox max min product single sum
* **Logic:** all any same whichever
* **Ordered:** changed concat first join last smudge
* **Statistics:** avg entropy median mode percentile stdev stdevp
* **Ranvar:** mixture ranvar ranvar.buckets sum
* **Zedfunc:** sum

* **Mathematics:** abs arground ceiling cos exp expsmooth floor log loggamma loglikelihood.loglogistic loglikelihood.normal loglikelihood.negativebinomial loglikelihood.poisson max min percent random.binomial random.integer random.loglogistic random.negativebinomial random.normal random.poisson random.shuffle random.uniform ratio round roundnext sin sqrt tanh
* **Text:** concat contains containsany containscount endswith escape field fieldcount fieldr indexof lowercase padleft parsedate parsenumber parsetime printtime replace startswith strlen substr text trim tryparsedate tryparsenumber tryparsetime tryparseweek uppercase
* **Calendar:** chineseyear chineseyearend chineseyearstart date daynum format isoyear monday month monthend monthnum monthstart today week weekNum year yearend yearstart
* **Ranking:** argfirst arglast assoc.quantity cumsub cumsubfallback cumsum fifo priopack rank rankd smudge
* **Graph:** canonical connected hascycles noncanonical partition
* **Ranvar:** actionrwd.demand actionrwd.segment cdf crps dirac dispersion exponential fillrate forest.regress int loglogistic mean mixture negativebinomial normal poisson quantile random.ranvar ranvar ranvar.periodicr ranvar.segment ranvar.uniform smooth spark support.min support.max transform truncate variance
* **UX:** Slices sliceSearchUrl
* *Zedfunc:** actionrwd.reward constant diracz int linear pricebrk.f pricebrk.m stockrwd.c stockrwd.m stockrwd.s uniform uniform.left uniform.right valueAt zoz
* **Table:** by extend.billOfMaterials extend.pairs extend.pairset extend.range extend.ranvar extend.split single by whichever by
* **64-sets**: flag emptySet union intersection complement isSubsetOf contains printSet popCount.
* **Special:** assertfail Files forex lastforex hash iscurrency mkuid nameof rgb solve.moq

### Grammer Chapters

* Relational algebra
* Natural joins
* Filtering
* Aggregating
* Secondary dimensions
* Cross tables
* Table comprehensions
* Table sizes
* Ranvars and Zedfuncs
* Enum Types
* Loops and iterations
* User defined functions
* Monte Carlo (`montecarlo` blocks)
* Differentiable Programming (`autodiff` blocks)
* Modules
* Read and write files
* Read dimensions
* Read patterns
* Read formats
* Path schemas
* Named schemas
* Dashboards
* Slicing dashboards
* Calendar Elements
* Read user inputs
* Tile syntax
* List of icons
* StyleCode
