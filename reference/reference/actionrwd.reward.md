+++
title = "actionrwd.reward"
+++

## actionrwd.reward(..) 🡒 (ranvar, zedfunc), process

The action reward function `actionrwd.reward()` returns a ranvar and a zedfunc aligned with marginal outcomes of the n<sup>th</sup> unit being ordered. The first zedfunc, the _demand_, is the probability distribution of the demand that is not yet served by the stock on hand and stock on order, within the relevant time frame. The second zedfunc, the _holding time_, is the expected number of periods where the unit will be kept in stock. The action reward emphasizes a discrete demand and lead time model centered around a single SKU.

See [actionrwd.demand](../actionrwd.demand/) and [actionrwd.segment](../actionrwd.segment/).

### Overview

The _action reward_ function is intended to compute the profitability of ordering one more unit of stock for a given SKU taking into account a probabilistic demand forecast, a probabilistic lead time forecast and a few other variables. This function is intended to be composed with a short series of economic variables as the expected marginal reward, the per-period carrying cost and the stock-out penalty. However, those variables are composed _externally_ and are not part of the action reward itself.

The action reward superseeds the _stock reward_. The action reward properly handles (a) non-stationary future demand, (b) non-deterministic leadtime, (c) fine-grained information about the stock on order and its estimated arrival time, (d) decoupled ordering lead times and supply lead times and (e) an ownership perspective the economic consequence of the decision.

* The _action reward_ models the probabilistic future demand through a trajectory generation mechanism which supports non-stationary patterns to be applied such as seasonality, trend or lifecycle.
* The lead time also benefits from a probabilistic modeling. This ensures that the reward estimate properly factor the risk of delays associated to the incoming orders.
* The stock on order is modeled explicitly with a time component which reflects the estimated arrival date of the incoming batch(es). The model backing the action reward implicitly assumes that the unserviced demand is _lost_ not merely delayed.
* The ordering frequency is distinguished from the supply lead time, instead of lumping the two lead time values together.
* The “ownership” perspective means that each +1 ordering increment is assessed in its capacity to serve the demand in a way that a _later_ decision _could not_. Yet, it assigns all the resulting carrying costs to this original decision.

The action reward function operates in the _ordering space_, that is, it estimates the marginal economic returns of ordering 0, 1, 2, … units of stocks. This perspective is slightly different from the stock reward function which was operating in the _stocking space_, that is, estimating the economic returns of having 0, 1, 2, … units _committed to the stock_.

The notion of _horizon_ in the action reward diverges in subtle but important ways compared to how the same notion is leveraged in the stock reward.

From the action reward perspective, at the level of a decision, the horizon is defined from an ownership (i.e. responsibility) perspective, and this horizon varies depending whether margin and stock-out penalty are considered vs. the carrying cost. For the margin and the stock-out penalty, the action is only “rewarded” (positively or negatively) for a duration equal to the ordering lead time. For the carrying cost, the action penalized for the entire lifetime of the unit held in stock.

### Concepts

The _period_ can be a day, a week or a month. The action reward is agnostic of the chosen time granularity.

The _coverage timespan_ starts at the point of time (in the future) when the first order passed today would be received and ends at the point of time (later in the future) where a second order passed at the next reorder opportunity would be received. From a decision-making perspective, the "upside" availability-wise of the present order is limited to the coverage timespan. Indeed, before this timespan, the present order is already too late to prevent the stockout; after this timespan, the prevention of the stockout becomes the responsibility of the next order.

The _demand_ estimates the probability distribution of the demand that is not covered yet by existing stock and that happens within the coverage timespan. This ranvar may have non-zero probabilities in the negative values: this simply means that even if no order is placed, the entire demand might still be covered, with stock remaining at the end of the coverage timespan.

From an economic perspective, the demand through drives both the gross margin and the stockout penalty. Indeed, if the unit isn't serviced within the coverage timespan, then, its gross margin does not _belong_ to the present order but to a later order. Conversely, if the unit is serviced within the coverage timespan, then, it means that lacking this unit would have generated a stockout. Thus, while gross-margin and stockout may appear as two distinct economic drivers, we see that, from the action reward perspective, those two factors are largely correlated.

The _holding timespan_ (or simply holding time) starts at the point of time (in the future) when a unit ordered today is received and ends at the point of time (later in the future) when this unit is finally serviced. From a desision-market perspective, the "downside" carrying-cost-wise of the present order runs for the whole holding timespan. Indeed, the action reward assumes that the only way to lower the stock is to service the demand, and thus, later orders can't "undo" a prior ordered stock quantity lingering around.

The _holding time_, as computed by the action reward function, is the mean of the distribution of holding timespan.

### Model details

The action reward makes multiple assumptions about the underlying SKU being modeled:

* A lead time deviate of 1 indicates that the goods will be available _at the start_ of the next period, hence prior to any consumption of stock for this period. More generally, received goods for a period are always assumed to be available at the beginning of the period. The same principle holds for the _stock on order_ whic represents past not-yet-fulfilled orders.
* A lead time deviate of 0 (zero) indicates that the goods will be available at the start of the _present_ period.
* A fraction of the demand is considered _lost_ whenever the demand for the period exceeds the stock available for this period. The lost demand is assumed to be non-recoverable, hence it cannot be serviced by a later arrival of good.

### Code example

```envision
table Items = with
  [| as Id, as SellPrice, as BuyPrice, as LeadTime, as ReorderFrequency, \
     as MeanDemand, as Dispersion, as StockAvailable, as StockOnOrder |]
  [| "cap",      20, 10,    5,  3,  12.1,  3.2,   3,  0 |]
  [| "hat",      10,  3,   10,  7,   2.4,  1.5,   0, 10 |]
  [| "t-shirt",  25, 10,   30,  7,   7.9,  2.3,   7,  2 |]

table Periods = extend.range(80 into Items) // days ahead

Periods.StockOnOrder = if Periods.N == 10 then Items.StockOnOrder else 0

Periods.Seasonality = match Periods.N with
  ..    13 -> 0.5
  14 .. 39 -> 1.5
  ..       -> 0.5

Periods.Baseline = Items.MeanDemand * Periods.Seasonality

Items.Alpha = 0.3

Items.Demand, Items.HoldingTime = actionrwd.reward(
  TimeIndex: Periods.N
  Baseline: Periods.Baseline
  Dispersion: Items.Dispersion
  Alpha: Items.Alpha
  StockOnHand: Items.StockAvailable
  ArrivalTime: dirac(Periods.N)
  StockOnOrder : Periods.StockOnOrder
  LeadTime: dirac(Items.LeadTime)
  StepOfReorder: Items.ReorderFrequency)

Periods.D = actionrwd.demand(
  Baseline: Periods.Baseline
  Dispersion: Items.Dispersion
  TimeIndex: Periods.N
  Alpha: Items.Alpha)

Periods.Median = quantile(Periods.D, 0.5)
Periods.Q95 = quantile(Periods.D, 0.95)
Periods.Q05 = quantile(Periods.D, 0.05)

oosPenalty = 0.4     // % relative to selling price
carryingCost = 0.005 // % per-period carrying cost relative to purchase price
Items.M = Items.SellPrice - Items.BuyPrice
Items.S = oosPenalty * Items.M
Items.C = carryingCost * Items.BuyPrice
Items.SellThrough = (1-cdf(Items.Demand + 1)) * uniform.right(1)
Items.R = Items.SellThrough * (Items.M + Items.S) - Items.HoldingTime * Items.C

table Slices[slice] = slice by id title: id

show scalar "Reward" a1c3 slices: Items.slice with same(Items.R) * uniform(0, 100)
show plot "Demand" a4c6 slices: Items.slice with
  Periods.N
  Periods.Median
  Periods.Q05
  Periods.Q95
```

### State space model of the demand

The demand trajectories are generated by a state space model. A single hidden state - the level - is used and generates observations in sequence. Each newly generated observation is drawn from a probability distribution - here a negative binomial - and this observation is used to update the state.

The pseudo-code that governs the state is given by:

```c
level[t = 0] = 1

foreach t:
  mean[t]        = baseline[t] * level[t]
  variance[t]    = mean[t] * dispersion
  observation[t] = DrawNegativeBinomial(mean[t], variance[t])
  level[t + 1]   = (1 - alpha) * level[t] + alpha * observation[t] / baseline[t]
```

If `alpha = 0`, the state space model is equivalent to a sequence of negative binomial distributions with `mean = baseline[t]` and `variance[t] = baseline[t] * dispersion`.

The number of trajectories used is also an input of the computation : the more trajectories, the more precise the computation, but also the longer it takes to compute. Similarly to the horizon, it is always beneficial to the precision to increase the number of trajectories, but past a certain point the precision gain becomes negligible.

### Function signature

```envision-proto
/// Returns two zedfuncs associated to the marginal outcome of ordering units. 
/// The space considered is the ordering space.
call actionrwd.reward<Items, Periods, Orders>(
    /// Defines a non-ambiguous ordering per item (i.e. distinct values required).
    Periods.TimeIndex: number as "TimeIndex",
    /// The baseline of the average demand over each period.
    Periods.Baseline: number as "Baseline",
    /// The dispersion parameter (variance divided by mean) of the demand for each item.
    Items.Dispersion: number as "Dispersion",
    /// The update speed parameter of the ISSM model for each item.
    Items.Alpha: number as "Alpha",  
    /// Stock on hand at the time the order is placed.
    Items.StockOnHand: number as "StockOnHand",
    /// Lead time, unit is abitrary time step, must be consistent with StepOfReorder.
    /// - Provided alone [legacy]: lead times used in the computation will be deviates sampled
    ///   from this distribution;
    /// - In conjunction with "NumLeadTime": lead times are still drawn from this
    ///   distribution, but deviates will be shifted by the fixed amount defined in
    ///   "NumLeadTime".
    Items.LeadTime?: ranvar as "LeadTime",
    /// Estimated next reorder time, in arbitrary time steps.
    Items.StepOfReorder: number as "StepOfReorder",
    /// Probability for each unit of demand to be covered by downstream stock.
    Items.StockOffHand?: zedfunc as "StockOffHand",
    /// Estimated order’s arrival period, zero-indexed.
    /// ArrivalTime and StockOnOrder must be both present, or both absent.
    Orders.ArrivalTime?: ranvar as "ArrivalTime",
    /// Quantity associated to the pending order. Stock is assumed available at the beginning of the period. 
    Orders.StockOnOrder?: number as "StockOnOrder",
    /// Number of trajectories used to evaluate to action reward.
    /// The parameter has to be defined within [1, 10'000]. Default: 2'500.
    scalar.Samples?: number as "Samples",  
    /// Seed used for the trajectory generator.
    scalar.Seed?: number as "Seed",    
    /// Lead time represented as a fixed numerical value.
    /// If provided alone, the fixed lead time specified will be the only
    /// value used in the computation. Please refer to "LeadTime" documentation
    /// for description of additional cases.
    Items.NumLeadTime?: number as "NumLeadTime"
    Items -> Periods,
    ?Items -> Orders) : {
        /// Serviceable demand on the responsibility window.
        Items.Demand: ranvar,
        /// Mean estimate of the number of periods of carrying cost for the nth
        /// ordered unit.
        Items.HoldingTime: zedfunc
    } as "actionrwd.reward"
```

### Annex: Fillrate

The fillrate is ratio between the expected sales and the expected demand over the coverage timespan. The naive application of the [fillrate](../../def/fillrate/) function directly to the `demand` output does not yield the intended result. Indeed, there is a part of the demand that is satisfied by the stock on hand and stock on order, hence the baseline is off.

Instead, the fillrate function should be applied to another ranvar called `TotalDemand`, which can be seen as an estimate of the total demand over the coverage timespan. The average expected `TotalDemand` is equal to the sum of the baselines over the time window of interest, and the shape of the `TotalDemand` is the same as the shape of the `demand` output. Therefore, to compute the estimation of the `TotalDemand`, one must right shift the `demand` ranvar up until its average is equal to baselines sum. The value of the shift can be interpreted as the expected demand that is already satisfied by existing stock, we call it `SatisfiedDemand`.

The fillrate function can then be applied to the `TotalDemand`. The current fillrate (the fillrate if no order is placed) is equal to the sum of the fillrate increments between 1 and `SatisfiedDemand`. The increments of fillrate generated by newly placed orders are the fillrate increments starting from `SatisfiedDemand+1`.

If the`SatisfiedDemand` is not an integer, we round it since ranvars in Envision can only be shifted by integers.

Example (to be appended to the above sample script) :

```envision
Items.MeanPriorDemand = sum(Periods.Baseline)
  when (Periods.N >= Items.LeadTime and 
        Periods.N < Items.LeadTime + Items.ReorderFrequency)
Items.SatisfiedDemand = Items.MeanPriorDemand - mean(Items.Demand)
Items.TotalDemand = Items.Demand + round(Items.SatisfiedDemand)
Items.Fillrate = fillrate(Items.TotalDemand)

Items.NewOrder = 3
Items.CurrentFillrate = int(Items.Fillrate, 1, Items.SatisfiedDemand)
Items.NewFillrate = int(Items.Fillrate, 1, Items.SatisfiedDemand+Items.NewOrder)

Items.TextId = text(Items.Id)
show table "Fillrates" with Items.TextId, Items.CurrentFillrate, Items.NewFillrate
```

<!--   

### Annex: Fillrate computation, demonstration

#### Definitions

* $$s_0$$ is the initial stock.

* $$r_0$$ is the order placed now that is received at time $$t_0$$.

* $$\mathbf{Y}$$, demand distribution between $$t_0$$ and $$t_1$$.
* $$S$$, distribution of the number of units sold between $$t_0$$ and $$t_1$$.
* $$X$$, stock distribution probability at $$t_1$$ if no order is placed to arrive at time $$t_0$$ (can be negative).
* $$P_Y$$ is equal to $$1-cdf(Y)$$, with Y a probability distribution. If $Y$ is the probability distribution of a demand, $$P_Y(k)$$ is the probability that the k-th unit is going to be sold.
* $$F$$, fillrate between $$t_0$$ and $$t_1$$.

The fillrate is defined as the expected number of sales divided by the expected demand :

$$F = \frac{\mathbb{E}[S]}{\mathbb{E}[\mathbf{Y}]}$$

What we want is the function that links the quantity we order to the fillrate :
$$F(s, r) = \frac{\mathbb{E}[S | s_0 = s, r_0 = r]}{\mathbb{E}[\mathbf{Y}]}$$

The expected sales is equal to the expected sales if we were to order nothing, plus the probability of selling each additional unit ordered.
$$\mathbb{E}[S | s_0 = s, r_0 = r] = \mathbb{E}[S | s_0 = s, r_0 = 0] + \sum_{k = 1}^{r} P_X(k)$$

The envision $$\mathtt{fillrate}$$ function computes, from a probability distribution $$Y$$:
$$\mathtt{fillrate}(Y, r) = \frac{\sum_{k = 1}^{r} P_Y(k)}{\sum_{k = 1}^{\infty} P_Y(k)} = \frac{\sum_{k = 1}^{r} P_Y(k)}{\mathbb{E}[Y]}$$

#### Demonstration
Our goal is to retrieve the actual fillrate function using only $$\mathbb{E}[\mathbf{Y}]$$, the Envision $$\mathtt{fillrate}$$ function, and $$X$$, the output of the action reward function.
Lets try to build a distribution $$Y$$ and a constant $$C$$, so that $$\mathtt{fillrate}(Y, C + r) = F(s, r)$$.

$$F(s, r) = \frac{\mathbb{E}[S | s_0 = s, r_0 = 0]}{\mathbb{E}[\mathbf{Y}]} + \frac{\sum_{k = 1}^{r} P_X(k)}{\mathbb{E}[\mathbf{Y}]}$$

Therefore :

$$F(s, r+1) - F(s, r) = \frac{\sum_{k = 1}^{r+1} P_X(k)}{\mathbb{E}[\mathbf{Y}]} - \frac{\sum_{k = 1}^{r} P_X(k)}{\mathbb{E}[\mathbf{Y}]} = \frac{P_X(r+1)}{\mathbb{E}[\mathbf{Y}]}$$

Moreover :$$\mathtt{fillrate}(Y, C + r) = \frac{\sum_{k = 0}^{C+r} P_Y[k]}{\mathbb{E}[Y]}$$

Therefore :

$$\mathtt{fillrate}(Y, C + r + 1) - \mathtt{fillrate}(Y, C + r) = \frac{\sum_{k = 0}^{C+r+1} P_Y[k]}{\mathbb{E}[Y]} - \frac{\sum_{k = 0}^{C+r} P_Y[k]}{\mathbb{E}[Y]} = \frac{P_Y[r+1]}{\mathbb{E}[Y]}$$

Therefore a necessary and sufficient condition for $$Y$$ to exist is that $$\forall r$$ :
$$\frac{P_Y[r+1]}{\mathbb{E}[Y]} = \frac{P_X(r+1)}{\mathbb{E}[\mathbf{Y}]}$$

We consider the distribution $$Y$$, defined as the distribution $$X$$ translated by the value $$C$$ so that $$\mathbb{E}[Y]$$ is equal to $$\mathbb{E}[\mathbf{Y}]$$. If it exists, then $$P_{Y}[r+1] = P_X(r+1)$$ and $$\mathbb{E}[Y] = \mathbb{E}[\mathbf{Y}]$$. Therefore $$\mathtt{fillrate}(Y, C + r + 1) - \mathtt{fillrate}(Y, C + r) = F(s, r+1) - F(s, r) $$  is true for all $$r$$, and $$\mathtt{fillrate}(Y, C+r) = F(s,r)$$.

Please note that if $$\mathbb{E}[\mathbf{Y}] - \mathbb{E}[X]$$ is not an integer, the $$Y$$ distribution does not exist. However, for our use cases, we can simply round $$\mathbb{E}[\mathbf{Y}] - \mathbb{E}[X]$$, and shift $$X$$ by this rounded value to obtain $$Y'$$. $$\mathtt{fillrate}(Y', C+r)$$ is then an excellent approximation of $$F(s,r)$$.

-->

### Annex: multi-echelon systems, actionrwd.dampen, and stockOffHand


StockOffHand is an optional argument of the action reward function. It is a zedfunc that represents what can be seen as the ‘stochastic’ stockOnHand, which reflects the stock available at a downstream echelon of the supply chain. See [actionrwd.dampen](../actionrwd.dampen/) for more details.
