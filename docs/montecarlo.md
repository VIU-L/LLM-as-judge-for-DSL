+++
title = "Monte Carlo"
description = ""
weight = 7
+++

In computing, _Monte Carlo_ broadly refers to the use of randomness as part of the logic. Randomized algorithms are of high interest for simulators and their specific uses in supply chain. Envision features extensive capabilities geared towards the use of randomness.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Overview

Envision features a series random functions, as illustrated by the following script:

```envision
table T = extend.range(10)
where random.binomial(0.5 into T)
  show table "" a1b6 with
    T.N
    random.normal(1 into T, 2)
```

In the above script, `random.binomial` is used to randomly select the lines of the table `T` with a probability of 0.5. The filtered table `T` is finally displayed with deviations drawn from a normal distribution of mean `1` and standard deviation `2`.

Re-running the script above yields the same numerical results. This behavior is intended and is discussed in greater details in the following section.

Repeatedly calling, in the same script, the same random function yields different results. However, beware of not broadcasting a unique random value over a whole table unless it’s the intended logic:

```envision
a = random.uniform(0, 1)
b = random.uniform(0, 1) 
show summary "" a1a2 with a, b // a != b (almost alway)

table T = extend.range(3)
T.X = random.uniform(0, 1) // WRONG!
show table "" b1b3 with T.X // all values are identical
```

In the above script, all the `T.X` values are identical because it’s the same scalar value `random.uniform(0, 1)` which was broadcast over the whole table. This script can be fixed with:

```envision
a = random.uniform(0, 1)
b = random.uniform(0, 1)
show summary "" a1a2 with a, b // a != b (almost always)

table T = extend.range(3)
T.X = random.uniform(0 into T, 1) // CORRECT!
show table "" b1b3 with T.X // distinct values (almost always)
```

In the above script, the expression `random.uniform(0 into T, 1)` evaluates directly on the table `T` and thus generates a series of distinct values.

## Pseudo-randomness

There is no “true” randomness involved in Envision, only pseudo-randomness: scripts remain strictly deterministic even when random functions are involved. Deterministic execution is of critical importance from a maintenance perspective. Without determinism, troubleshooting defective logic becomes a fairly uncertain undertaking for whoever is in charge of maintaining a given Envision script.

The Envision runtime guarantees that if the data hasn’t changed and if the script hasn’t changed, then the results don’t change either. However, even the slightest change to the data effectively “resets” the pseudo-randomness that surfaces in the execution of the script.

Under the hood, the pseudo-randomness depends on an initial integer that is used to initialize the source of randomness. In computing, this integer is commonly referred to as a _seed_. Envision abstracts away entirely the need to manually manage the seeds.

The runtime of Envision, which may span the execution over multiple machines, ensures that no accidental indeterminism gets introduced while distributing the computations.

## `montecarlo` blocks

The `montecarlo` block is a variant of the `each` block dedicated to randomized logic. This block offers the possibility to collect _accumulated_ values over many scenarios. The following script computes a (very) approximate value of $\pi$ through a Monte Carlo process:

```envision
montecarlo 1000 with
  x = random.uniform(-1, 1)
  y = random.uniform(-1, 1)
  inCircle = x^2 + y^2 < 1
  sample approxPi = avg(if inCircle then 4 else 0)
show scalar "π approximation" with approxPi
```

In the above script, the keyword `montecarlo` is used to introduce the block of iterated logic. The number of interactions appears as an integer right after the `montecarlo` keyword. In the block itself, two random numbers are obtained from the uniform distribution. Finally, the `sample` keyword is used to declare the accumulator, which is used to expose and return the results of the `montecarlo` block.

The value that follows the keyword `montecarlo` must be a constant scalar.

The keyword `sample` introduces an assignment of the form `sample T.foo = avg(T.expr)`, the aggregation being relative to the iterations of the `montecarlo` block. This mechanism should not be confused with a regular aggregation followed by a broadcast. In particular, the statement `T.foo = avg(T.expr)` is not equivalent to the statement `sample T.foo = avg(T.expr)`.

A single `montecarlo` block can introduce multiple accumulators. A `montecarlo` block can be nested inside an `each` block, and vice versa.

The previous script is logically equivalent to:

```envision
table T = extend.range(1000)
sum = 0
each T scan T.N
  keep sum
  x = random.uniform(-1, 1)
  y = random.uniform(-1, 1)
  inCircle = x^2 + y^2 < 1
  sum = sum + (if inCircle then 4 else 0)
approxPi = sum / 1000
show scalar "π approximation" with approxPi
```

However, the above script, which relies on an `each` block, requires the explicit creation of a table `T`, which is avoided when a `montecarlo` block is used instead. As a rule of thumb, it is advised to leverage a `montecarlo` block when dealing with Monte Carlo processes. The intent is clearer and the compute performance is better.

The `sample` keyword can also be used to collect data from any `small` table, as illustrated by:

```envision
table T = extend.range(5)
montecarlo 1000 with
  T.K = random.poisson(T.N)
  sample T.ApproxMean = avg(T.K)
show table "Poisson means" a1b5 with T.N, T.ApproxMean
```

Two accumulators are supported `avg()` and `ranvar()` by the `sample` assignment.

**Roadmap:** More diverse accumulators will be introduced in the future.

## Illustration: Innovation State Space Model (ISSM)

Innovation state space models (ISSM) are a class of time series generative models which are suitable for probabilistic forecasting from a supply chain perspective. Despite the impressive-sounding name, ISSMs are simple: a state vector $s_t$ evolves over time adding small random _innovations_ at each step.

Formally, let $\mathcal{F}$ be a random function that takes two arguments $\theta_t$ (the parameters) and $s_t$ (the state).  Let $z_t$ be the deviate generated by the ISSM model at time $t$:

$$z_t \sim \mathcal{F}(\theta_t, s_t) $$

Let $\alpha \in ]0,1[$ be the smoothing parameter. The state transition function that governs the state vector is given by:

$$s_{t+1} = \alpha \frac{z_t s_t}{E\left[\mathcal{F}(\theta_t,s_t)\right]} + (1 - \alpha) s_t$$

where $E[..]$ is the expected value.

The parameter $\theta_t$ governs the "shape" of the ISSM. In practice, this parameter is used to reflect common patterns such as the trend, the seasonality, the day of the week ... Learning the $\theta_t$ values, as well as the initial state $s_0$, can be done via differentiable programming which will be discussed in a later section.

The following script illustrates an ISSM governed by a negative binomial distribution used as the random function:

<!-- TODO: screenshot of the ISSM -->
```envision
keep span date = [date(2021, 8, 1) .. date(2021, 10, 30)]

Day.Baseline = random.uniform(0.5 into Day, 1.5) // 'theta'
alpha = 0.3
level = 1.0 // initial level
minLevel = 0.1
dispersion = 2.0

Day.Q = each Day scan date // minimal ISSM
  keep level
  mean = level * Day.Baseline
  deviate = random.negativeBinomial(mean, dispersion)
  level = alpha * deviate / Day.Baseline + (1 - alpha) * level
  level = max(minLevel, level) // arbitrary, prevents "collapse" to zero
  return deviate

show linechart "" a1d3 with Day.Q
```

However, a single generated time series is of little use in practice. The ISSM is intended to be used to generate many time series, referred as _trajectories_, which are then used to perform arbitrary measurements. For example, let's say that we want to measure the probability of having exactly zero unit of demand over the last 10 days of the period of interest. Moreover, let's say that we want to process multiple SKUs at once. This can be done with:

```envision
keep span date = [date(2021, 8, 1) .. date(2021, 10, 30)]

table Sku = extend.range(10)
table SkuDay = cross(Sku, Day)
SkuDay.Baseline = random.uniform(0.5 into SkuDay, 0.5 + Sku.N) // 'theta'
dispersion = 2.0
alpha = 0.3
level = 1.0 // initial level
minLevel = 0.1
 
Sku.IsLast10zero = each Sku
  Day.Baseline = SkuDay.Baseline
  montecarlo 1000 with
    Day.Q = each Day scan date
      keep level
      mean = level * Day.Baseline
      deviate = random.negativeBinomial(mean, dispersion)
      level = alpha * deviate / Day.Baseline + (1 - alpha) * level
      level = max(minLevel, level)
      return deviate
    // unit sold over the last 10 days
    total = sum(Day.Q) when (date > date(2021, 10, 20))
    sample isLast10zero = avg(if total == 0 then 1 else 0)
  return isLast10zero
 
show table "Odds of zero sales over Oct 21th to Oct 30th" a1c8 with 
  Sku.N
  Sku.IsLast10zero
```

In the above script, the ISSM is used to generate 1000 trajectories for every SKU. The probability is empirically measured over those trajectories. The baseline `SkuDay.Baseline` is intentionally constructed to increase along with `Sku.N`. This explains why `Sku.IsLast10zero` decreases while `Sku.N` increases.
