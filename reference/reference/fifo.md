+++
title = "fifo"
+++

## fifo(T.onHand: number, U.purchDate: date, U.purchQty : number) 🡒 U.unitByAge : number, process

Returns the number of units that still remain from the historical purchase orders assuming a FIFO (first-in, first-out) consumption.

```envision
table P[id] = with
  [| as Id, as OnHand |]
  [| "hat", 5 |]
  [| "cap", 4 |]

table T = with
  [| as Pid, as PurchDate, as PurchQty |]
  [| "hat", date(2020, 8, 20), 6 |]
  [| "hat", date(2020, 7, 15), 3 |]
  [| "cap", date(2020, 8, 12), 1 |]
  [| "cap", date(2020, 8, 3),  1 |]
  [| "cap", date(2020, 8, 1),  5 |]

where T.Pid in id
  T.Fifo = fifo(P.OnHand[T.Pid], T.PurchDate, T.PurchQty)

  show table "" a1e6 with
    T.Pid
    P.OnHand[T.Pid]
    T.PurchDate
    T.PurchQty
    T.Fifo
    order by [T.Pid, -T.PurchDate]
```

The `fifo` function could also be rewritten with a user-defined process:

```envision
table P[id] = with
  [| as Id, as OnHand |]
  [| "hat", 5 |]
  [| "cap", 4 |]

table T = with
  [| as Pid, as PurchDate, as PurchQty |]
  [| "hat", date(2020, 8, 20), 6 |]
  [| "hat", date(2020, 7, 15), 3 |]
  [| "cap", date(2020, 8, 12), 1 |]
  [| "cap", date(2020, 8, 3),  1 |]
  [| "cap", date(2020, 8, 1),  5 |]

keep where T.id = T.Pid

def process fifo_bis(qty: number; onHand: number) with
  keep rest = onHand
  sourced = min(rest, qty)
  rest = rest - sourced
  return sourced

T.MyFifo = fifo_bis(T.PurchQty; P.OnHand) by id scan (-T.PurchDate)

show table "" a1e6 with
  T.Pid
  P.OnHand[T.Pid]
  T.PurchDate
  T.PurchQty
  T.MyFifo
  order by [T.Pid, -T.PurchDate]
```

## See also

* [The FIFO inventory methdo](../../../library/fifo-inventory-method/)
