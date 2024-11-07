+++
title = "actionrwd.dampen"
+++

The inventory control of multi-echelon systems is notoriously difficult. Optimizing replenishment decisions in single-echelon systems is much simpler. The intent behind the `actionrwd.dampen` function is to simplify the replenishment decision-making at the upper level of a two-echelon system, by abstractly representing its network as an approximately equivalent single-echelon system. The idea of this approximation is to encapsulate all the relevant information about the stock levels at the lower level of the network into an abstract high-level variable, the StockOffHand.

## actionrwd.dampen(..) 🡒 zedfunc, process

In a 2-echelon supply network, the function `actionrwd.dampen` returns the fraction of the upstream demand which is already serviced by downstream stocks in a 2-echelon network. The returned zedfunc is indexed by the overall upstream demand. This function is expected to be decreasing as stock-outs happen downstream.

### The 2-echelon supply network model

The supply network of interest is expected to have two echelons, the upper echelon being referred to as a single warehouse, the lower echelon being referred to as stores. Both the warehouse and the stores are holding stock. Supplies can be dispatched from the warehouse to the stores when necessary, but supply cannot be transferred from stores to the warehouse, or to other stores.

Demand-wise, there are two situations:

* Either the demand only happens at the lower echelon, i.e. only stores serve demand.
* Or the demand happens on both echelons, i.e. the warehouse and the stores both serve demand.

In the following, those two situations are reviewed.

### The StockOffHand: a probabilistic equivalent to the stock available in the network

The objective is to compute the economic impact of replenishing the stocks at the warehouse level. Replenishment orders (at warehouse level) are expected to cover the demand over the entire network. These replenishment orders should account for the fact that stores can act as buffers based on their own local stocks.

In Envision, the economic impact of replenishment decisions in single-echelon systems is usually determined with the [actionrwd.reward](../actionrwd.reward/) function. This function notably estimates the probability distribution of the demand - per sku - that has to be serviced during a responsibility time window, and that is not yet covered by stock on hand or on order. We refer to this quantity as the `SkuUncoveredDemand`. In a single echelon system, the `SkuUncoveredDemand` is simply equal to the sku demand during the responsibility window minus the sku available stock at the beginning of the responsibility window.

The purpose of the _dampen_ function is to enable the useof the `actionrwd.reward()` function to compute the equivalent `SkuUncoveredDemand` for a 2-echelon network.

In a two-echelon system, the sku demand in the network equals the sum of the demand in all the stores. However, the demand may not be covered even if the available stock in all the stores is not depleted yet. For example, if one store is out of stock at the beginning of the responsibility window, but the other stores are not, the warehouse is responsible for covering the demand of this particular store. In a two-echelon system, the `SkuUncoveredDemand` can therefore not be written as the demand during the responsibility window minus the available stock at the beginning of the responsibility window.

Instead, the `actionrwd.dampen()` model assigns a probability of already being covered by the network stock, to each unit of demand. The model considers the demand at the network level as it arrives, one unit of demand after the other. Each time a sku is demanded, it is demanded in a store, and this store is either out of stock, or sufficiently stocked to satisfy this unit of demand. The stockOffHand is a zedfunc, a function that associates to each unit of demand at network level $k$ the probability that the k-th unit of demand (at network level) is observed in a store that is not stocked-out yet, _regardless of the moment the demand occurs_ . This zedfunc is decreasing, and converges towards zero at infinity.

The StockOffHand can be seen as a stochastic equivalent to the single echelon available stock: it efficiently summarizes the stock available at the store level echelon of the supply chain. It can be used as an optional input of the `actionrwd.reward()` function, which uses it to compute the corresponding `SkuUncoveredDemand`.

### Modeling assumptions

Unlike the other `actionrwd` functions, here, three tables are introduced in order to reflect the two echelons:

* `Skus`: the SKUs at the warehouse level.
* `DownSkus`:  the SKUs are the store’s level.
* `DownPeriods`: a dowstream table of `DownSkus` which adds the time dimension.

The function `actionrwd.dampen()` assumes that future demand of every ‘DownSkus’ can be modeled through ISSM. This assumption is consistent with the other `actionrwd` functions.

`actionrwd.dampen()` makes the additional assumption that the dispersion and the alpha are the same for all the ‘DownSkus’ associated to the same ‘Sku’. Thanks to the properties of the negative binomial distribution, the demand over the entire network of any SKU also follows an ISSM, with a baseline equal to the sum of the associated DownSkus baselines, and an alpha and dispersion equal to the associated DownSkus alpha and dispersion.

`actionrwd.dampen()` has an optional argument ‘Samples’ (default 2'500) which sets the number of trajectories generated to compute the StockOffHand. Just like the other actionrwd functions, more samples equates to more accurate results (up to a certain point), but increases the computation time linearly.

#### Additional constraints

- Table `DownSkus` must be strictly larger than table `Skus`.
- All `StockOnHand` should be ≥ 0.
- The `BaseLine` should be ≥ 0.
- The `Horizon` should be ≤ 371.
- The `Alpha` should be between 0 and 1.
- The `Dispersion` should be between 1 and 1e7.
   - If `Dispersion` is 1, then `BaseLine` should be less than 67067853.
   - If `Dispersion` is greater than 1, then `BaseLine` and `Dispersion` should be valid arguments for `random.negativeBinomial`.
- All `TimeIndex` should be distinct. 
- All `DownSkus` for the same `DownSkus.
- The `Samples` should be an integer between 1 and 10000.
- The maximum number of downstream locations is 10000.

### Code example

```envision
table Skus = with
  [| as Id, as Dispersion, as Alpha |]
  [| "cap", 1.2,  0 |]
  [| "hat", 2.5, 0.01 |]

table Loc = with
  [| as Id |]
  [| "store1" |]
  [| "store2" |]

table DownSkus = cross(Skus, Loc) // Table Sku x Loc
DownSkus.StockOnHand = 0
DownSkus.Horizon = 52

table DownPeriods = extend.range(DownSkus.Horizon) // Table Sku x Loc x Time
DownPeriods.Baseline = 10

Skus.StockOffHand = actionrwd.dampen(
  TimeIndex: DownPeriods.N
  Baseline: DownPeriods.Baseline
  Dispersion: Skus.Dispersion
  Alpha: Skus.Alpha
  StockOnHand: DownSkus.StockOnHand)
```

### Function signature

```envision-proto
/// Returns the fraction of the upstream demand which gets serviced from
/// the downstream stock in a 2-echelon network.
call actionrwd.dampen<Items, DownItems, Periods>(
   /// The dispersion parameter (variance divided by mean) of the demand.
   Items.Dispersion: number as "Dispersion",
   /// The update speed parameter of the ISSM model, ranges within [0, 1].
   Items.Alpha: number as "Alpha",
   /// The downstream stock on hand.
   DownItems.StockOnHand: number as "StockOnHand",
   /// Defines a non-ambiguous ordering per downItem (i.e. distinct values required).
   Periods.TimeIndex: number as "TimeIndex",
   /// The baseline of the average demand over each period.
   Periods.Baseline: number as "Baseline",
   /// Number of trajectories used to evaluate the cumulative demand.
   /// The parameter has to be defined within [1, 10'000]. Default: 2'500.
   scalar.Samples?: number as "Samples",
   /// Seed used for the trajectory generator.
   scalar.Seed?: number as "Seed",
   Items -> Periods,
   DownItems -> Periods) : Items.zedfunc as "actionrwd.dampen"

```

### Annex: Demand only at the lower echelon

We provide an example script for the computation of the economic impact of replenishment decisions at the warehouse level, when the demand only occurs only at the lower echelon.

```envision
table Skus[Id] = with
  [| as Id, as Dispersion, as Alpha, as StockInWarehouse |]
  [| "cap", 1.2, 0.01, 2 |]
  [| "hat", 1.5, 0, 3 |]

// In practice the DownSkus table should be extracted from a file using a read statement.
table DownSkus = with
  [|     as Loc, as Id|]
  [| "Store1", Skus.Id |]
  [| "Store2", Skus.Id |]
table DownSkus[sku] = single by [DownSkus.Loc, DownSkus.Id]
DownSkus.StockOnHand = if DownSkus.Loc == "Store1" then 2 else 5

// In practice the DownSkusPeriods table should be extracted from a file using a read statement.
// Trivial example with only three time steps
table DownSkusPeriods = with
  [| as Id, as Loc, as N |]
  [| Skus.Id, DownSkus.Loc, 1 |]
  [| Skus.Id, DownSkus.Loc, 2 |]
  [| Skus.Id, DownSkus.Loc, 3 |]
expect DownSkusPeriods.sku = (DownSkusPeriods.Loc, DownSkusPeriods.Id)
DownSkusPeriods.Baseline = if DownSkusPeriods.Id=="cap" then 10 else 20

// Stock off hand computation
Skus.StockOffHand = actionrwd.dampen(
  TimeIndex: DownSkusPeriods.N
  Baseline: DownSkusPeriods.Baseline
  Dispersion: Skus.Dispersion
  Alpha: Skus.Alpha
  StockOnHand: DownSkus.StockOnHand)

table SkusPeriods = by [DownSkusPeriods.Id, DownSkusPeriods.N]

// The baseline of the demand in the entire network is the sum of the demand in each location
SkusPeriods.Baseline = sum(DownSkusPeriods.Baseline)
SkusPeriods.N = same(DownSkusPeriods.N)

// Action reward at warehouse level computation
Skus.SellThrough, Skus.HoldingTime = actionrwd.reward(
  TimeIndex: SkusPeriods.N
  Baseline: SkusPeriods.Baseline
  Dispersion: Skus.Dispersion
  Alpha: Skus.Alpha
  StockOnHand: Skus.StockInWarehouse
  LeadTime: dirac(0)
  StepOfReorder: 1
  StockOffHand: Skus.StockOffHand)


show table "Action reward primitives" with
  Skus.Id
  Skus.SellThrough
  Skus.HoldingTime
```

### Annex: Demand on both lower and upper echelons

If one observes demand at warehouse level, the usage of the `actionrwd.dampen()` must be adapted. Conceptually, the warehouse is divided into two different entities: the 'storage warehouse' and the 'store warehouse'. The 'storage warehouse' acts as a warehouse for all the stores, but has no associated demand. On the other hand, the 'store warehouse' is seen as an additional store, which holds no stock, but can be delivered instantly by the 'store warehouse' to cover its associated demand.

`actionrwd.dampen()` considers the 'store warehouse' as any other store (except that its DownSkus.StockOnHand is equal to zero) and computes the corresponding StockOffHand. `actionrwd.reward()` is then called with the StockOffHand input, and with the Skus.StockOnHand being the stock available at the 'store warehouse'. A code example is also provided. It is identical to the previous example, except for the StockOnHand inputs of both `actionrwd.reward()` and `actionrwd.dampen()`.

```envision
table Skus[Id] = with
  [| as Id, as Dispersion, as Alpha|]
  [| "cap", 1.2, 0.01 |]
  [| "hat", 1.5, 0 |]

// In practice the DownSkus table should be extracted from a file using a read statement.
table DownSkus = with
  [|     as Loc, as Id|]
  [| "Warehouse", Skus.Id |]
  [| "Store1", Skus.Id |]
table DownSkus[sku] = single by [DownSkus.Loc, DownSkus.Id]
DownSkus.StockOnHand = if DownSkus.Loc == "Store1" then 2 else 5

// In practice the DownSkusPeriods table should be extracted from a file using a read statement.
// Trivial example with only three time steps
table DownSkusPeriods = with
  [| as Id, as Loc, as N |]
  [| Skus.Id, DownSkus.Loc, 1 |]
  [| Skus.Id, DownSkus.Loc, 2 |]
  [| Skus.Id, DownSkus.Loc, 3 |]
expect DownSkusPeriods.sku = (DownSkusPeriods.Loc, DownSkusPeriods.Id)
DownSkusPeriods.Baseline = if DownSkusPeriods.Id=="cap" then 10 else 20

// The actionrwd.dampen() function considers that the 'store warehouse' is empty.
DownSkus.StockOnHandForDampen = if DownSkus.Loc=="Warehouse" then 0 else DownSkus.StockOnHand

// Stock off hand computation
Skus.StockOffHand = actionrwd.dampen(
  TimeIndex: DownSkusPeriods.N
  Baseline: DownSkusPeriods.Baseline
  Dispersion: Skus.Dispersion
  Alpha: Skus.Alpha
  StockOnHand: DownSkus.StockOnHandForDampen)

table SkusPeriods = by [DownSkusPeriods.Id, DownSkusPeriods.N]

// The baseline of the demand in the entire network is the sum of the demand in each location
SkusPeriods.Baseline = sum(DownSkusPeriods.Baseline)
SkusPeriods.N = same(DownSkusPeriods.N)

// The actionrwd.reward() function considers the 'storage warehouse' stock level
Skus.StockInWarehouse = same(DownSkus.StockOnHand) where DownSkus.Loc == "Warehouse"

// Action reward at warehouse level computation
Skus.SellThrough, Skus.HoldingTime = actionrwd.reward(
  TimeIndex: SkusPeriods.N
  Baseline: SkusPeriods.Baseline
  Dispersion: Skus.Dispersion
  Alpha: Skus.Alpha
  StockOnHand: Skus.StockInWarehouse
  LeadTime: dirac(0)
  StepOfReorder: 1
  StockOffHand: Skus.StockOffHand)


show table "Action reward primitives" with
  Skus.Id
  Skus.SellThrough
  Skus.HoldingTime
```
