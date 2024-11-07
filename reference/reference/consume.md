+++
title = "consume"
+++

## consume( requested : number; initial : number | requested : vector) 🡒 number, process

`consume(T.Requested; Initial)` returns for every line of `T`, how much of that request could actually be served given that the initial available quantity was `Initial`.

For instance, we have a request for `15` elements, and we have `3` available lots of `10` elements each which must be consumed in a specific order (e.g. because of expiration dates). What is the quantity of each lot that is consumed by the request?

We could express such a request in Envision as follows:

```envision-proto
Lots.QtyConsumed = consume(Lots.QtyAvailable; qtyRequested) scan Lots.Order
```

With the amounts defined above, this would return `10` for the first lot, `5` for the second lot, and `0` for the last lot.

It is also possible to use a vector instead of a scalar in the function call:

```envision-proto
Lots.QtyConsumed = consume(Lots.QtyAvailable; Items.QtyRequested) by id scan Lots.Order
```

### Note the semicolon `;` in the list of arguments

The arguments left of the semicolon are line-level arguments, the arguments right of it are group-level arguments. The arguments will be used for initializing internal process variables - the process does not work directly with the passed arguements themselves, the original sources will never be modified.

### Example

```envision
table Items[Id] = with
  [|as Id, as Stock|]
  [|"a", 10|]
  [|"b", 7|]


table Orders = with
  [|as OId, as Qty|]
  [|"a", 1|]
  [|"a", 1|]
  [|"a", 2|]
  [|"a", 1|]
  [|"b", 5|]
  [|"b", 10|]
  [|"b", 25|]

expect Orders.Id = Orders.OId

Orders.ServedFromStock = consume(Orders.Qty; Items.Stock) by Id scan Orders.*

show table "Orders" with
  Orders.Id
  Orders.Qty
  Orders.ServedFromStock
```

This example will produce the following output:

**Orders**

| Id | Qty | ServedFromStock |
|:----|---:|-----:|
| a | 1 | 1 |
| a | 1 | 1 |
| a | 2 | 2 |
| a | 1 | 1 |
| b | 5 | 5 |
| b | 10 | 2 |
| b | 25 | 0 |

**Note**: The `consume` function will **not** subtract the _consumed_ quantities from `Items.Stock`, it will only return the consumed quantities. In the above example, the consumed values returned by the function will be stored in the new table column `Orders.ServedFromStock`.

## See also

- [assoc.quantity](/reference/abc/assoc.quantity/)
