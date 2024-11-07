+++
title = "rank"
+++

## rank() scan T.s : 's 🡒 T.rk : number, process

Returns integers in ascending order, starting at 1, following the order given by the `scan`. Tie-breaks are arbitrary.

```envision
table T = with
  [| as N |]
  [| 0 |]
  [| 9 |]
  [| 3 |]
  [| 7 |]
  [| 3 |]

T.rk = rank() scan T.N

show table "" a1b4 with
  T.N
  T.rk
```

Outputs: 

| N | rk |  |
|---|---|---|
| 0 | 1 |
| 9 | 5 |
| 3 | 3 | _Arbitrary tie-break, could be '2'_
| 7 | 4 |
| 3 | 2 | _Arbitrary tie-break, could be '3'_

_Reminder_: the scan can include the [`desc` keyword](/reference/def/desc/) to reverse the order of one or more columns: 

```envision 
table T = with
  [| as N |]
  [| "A" |]
  [| "B" |]
  [| "C" |]
  [| "D" |]
  
T.rk = rank() scan [T.N desc]
 
show table "" a1b4 with
  T.N
  T.rk
```

Outputs: 

| N | rk 
|---|---|
| A | 4 
| B | 3
| C | 2
| D | 1 


## rank() by T.g : 'g scan T.s : 's 🡒 T.rk : number, process

Within each group defined with `by`, returns integers in ascending order, starting at 1, following the order given by the `scan`. Tie-breaks are arbitrary. Tie-breaks are arbitrary.

```envision
table T = with
  [| as N, as G |]
  [| 0, "a" |]
  [| 1, "a" |]
  [| 2, "b" |]
  [| 3, "b" |]

T.rk = rank() by T.G scan T.N

show table "" a1c4 with
  T.G
  T.N
  T.rk
```
Outputs: 

| G | N | rk |
|---|---|---|
| a | 0 | 1 |
| a | 1 | 2 |
| b | 2 | 1 |
| b | 3 | 2 |

## rank(T.n : 'n, T.g : 'g, T.s : 's) 🡒 T.rk : number, process

The purpose of this `rank` overload is to support the generation of a prioritized purchase list. In particular, this overload cannot be re-expressed as a simple expression of sorting and grouping. This is a two-stage imperative algorithm. In the first stage, values are grouped by `T.g` into stacks, with each stack ordered by ascending  `T.s`. In the second stage, the algorithm selects the highest value of `T.n` among the top elements of all stacks, pops that element, assigns it a rank (starting at 1), and repeats until all stacks are empty.

```envision
table T = with
  [| as N, as G, as S |]
  [| 0, "a", 1 |]
  [| 1, "a", 0 |]
  [| 2, "b", 1 |]
  [| 3, "b", 0 |]

T.rk = rank(T.N, T.G, T.S)

show table "" a1d4 with
  T.G
  T.N
  T.S
  T.rk
```
