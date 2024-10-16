+++
title = "Relational algebra"
description = "Envision is a hybrid between array programming and relational algebra. Envision is geared towards operations performed over relational databases, as commonly found in enterprise systems, but it also abstracts away the need for loops, both for performance and reliability purposes, as commonly done with array programming languages."
weight = 3
+++

Envision is a hybrid between array programming and relational algebra. Envision is geared towards operations performed over relational databases, as commonly found in enterprise systems, but it also abstracts away the need for loops, both for performance and reliability purposes, as commonly done with array programming languages.

Every variable in Envision belongs to a **table**, and technically, identifies a **vector**, that is, a collection of values with one value per table line. Thus, when two variables belong to the same table, it becomes possible to perform operations on all lines at the same time.

```envision
table Colors = with
  [| as French, as English |]
  [| "Rouge", "Red" |]
  [| "Bleu", "Blue" |]
  [| "Vert", "Green" |]

Colors.Explain = "\{Colors.French} means \{Colors.English}."

show table "My Translation" with Colors.Explain
```

The script above outputs a table that contains the 3 lines with the following content:

| Explain          |
|------------------|
| Rouge means Red  |
| Bleu means Blue  |
| Vert means Green |

The text format operation used to compute `Colors.Explain` has been done for all the lines of the `Colors` table at once.

Numeric operations can be performed in a similar way :

```envision
table Orders = with
  [| as Quantity, as UnitPrice |]
  [| 3, 12.00 |]
  [| 7, 20.50 |]
  [| 2, 25.00 |]

tax = 0.2
Orders.Charge = Orders.Quantity * Orders.UnitPrice * (1 + tax)

show table "Tax Included" with Orders.Charge
```

Which gives the resulting table:

| Charge |
|--------|
| 43.2   |
| 172.2  |
| 60     |

The attentive reader might have noticed that the script above is mixing _two_ tables in the calculation of `Orders.Charge`: the `Orders` table and the `Scalar` table, the latter being implicit for both `tax` and the `1` number literal. This mechanism is referred to as _broadcasting_, and will be detailed in the following.

A _vector_ in the Envision realm is equivalent to a _column_ in the database realm. However, unlike SQL databases, creating and manipulating columns in Envision is the natural expected way to proceed. By leveraging operations that are automatically performed over a vector (i.e. a column), Envision removes the need to resort to manual loops (i.e. `for` loops) in the vast majority of supply chain situations.

_Advanced remark_: Envision tables are what Python or R users would recognize as Data Frames. Under the hood, Envision does not _reify_ all the vectors, even when those vectors get named through a variable. For performance, the compiler attempts to inline calculations whenever inlining is deemed more efficient than the alternative. For example, renaming a vector i.e. `Orders.ChargeBis = Orders.Charge` is a zero-cost operation in Envision.

## Video Tutorial

<iframe width="640" height="360" sandbox="allow-same-origin allow-scripts allow-popups" src="https://tube.lokad.com/videos/embed/943f8aa9-75fc-435f-afa9-f178ca73038a?title=0&warningTitle=0" frameborder="0" allowfullscreen></iframe>
