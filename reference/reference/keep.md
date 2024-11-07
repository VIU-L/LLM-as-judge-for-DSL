+++
title = "keep"
+++

The keyword `keep` has two uses in Envision, either to avoid an identation, or to define the state of a process.

## 'keep where ..', block de-indentation

When the keyword `keep` appears at the start of a `where` statement, the filter applies until the end of scope.

```envision
table T = with
  [| as N |]
  [| 0 |]
  [| 1 |]
  [| 2 |]

keep where T.N < 2 // This filter applies until the end of the script (current scope).

show table "T1" with T.N // No indent. Display 0, 1.
show table "T2" with T.N // No-indent. Display 0, 1. (same)
```

Without the `keep`, the `where` block requires an indentation. The dedent implies exiting the filtered block.

```envision
table T = with
  [| as N |]
  [| 0 |]
  [| 1 |]
  [| 2 |]

where T.N < 2 // This filter applies until the end of the script.
  show table "T1" with T.N // Indent. Display 0, 1.

show table "T2" with T.N // No-indent (exiting the 'where' block). Display 0, 1, 2.
```

## 'keep span date = ..', unfiltering de-indentation

When the keyword `keep` appears at the start of a `span` statement, the unfilter applies until the end of the scope.

```envision
keep span date = [date(2024, 1, 1) .. date(2024, 1, 31)] // implicit creation of table 'Day'
Day.X = random.poisson(10 into Day) // mock random data
show linechart "L1" with Day.X // the time-series over 31 days
show linechart "L2" with Day.X // the time-series over 31 days (same)
```

Without the `keep`, the `span` block requires an indentation. The dedent implies existing the unfiltered block.

```envision
span date = [date(2024, 1, 1) .. date(2024, 1, 31)] // implicit creation of table 'Day'
  Day.X = random.poisson(10 into Day) // mock random data
  show linechart "L1" with Day.X // the time-series over 31 days
show linechart "L2" with Day.X // 'No data available for linechart'
```

## 'keep var = expr', state initialization in a process

At the beginning of a `process` block, the variables that are part of the state of the process can be declared with the keyword `keep`.

```envision
def process logSum(proba : number) with
  keep logP = 0 // declare 'logP' as part of the state, and initialize
  logP = logP + log(proba)
  return logP

table Probabilities = with
  [| as P |]
  [| 0.1  |]
  [| 0.6  |]
  [| 0.2  |]

// 'sort' is required, but has no consequence here (sum is commutative)
show scalar "log probability" with logSum(Probabilities.P) sort 1 // -4.42
```

## 'keep var', state declaration in a loop

In a `for` loop that enumerates the values of a column, the keyword `keep` is used to declare the variables part of the state of the loop:

```envision
table Probabilities = with
  [| as P |]
  [| 0.1  |]
  [| 0.6  |]
  [| 0.2  |]

logP = 0 // loop variable 'logP' is initialized above the loop
for p in Probabilities.P scan auto // ordering has no importance
  keep logP // declare 'logP' as part of the state of the loop
  logP = logP + log(p)

show scalar "log probability" with logP // -4.42
```

Idem, with a `each` loop, that enumerates the lines of a table:

```envision
table Probabilities = with
  [| as P |]
  [| 0.1  |]
  [| 0.6  |]
  [| 0.2  |]

logP = 0 // loop variable 'logP' is initialized above the loop
each Probabilities scan auto
  keep logP // declare 'logP' as part of the state of the loop
  logP = logP + log(Probabilities.P)

// 'sort' is required, but has no consequence here (sum is commutative)
show scalar "log probability" with logP // -4.42
```
