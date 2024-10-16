+++
title = "Differentiable Programming"
description = ""
weight = 8
+++

Differentiable programming (DP) is a programming paradigm at the intersection of _machine learning_ and _numerical optimization_. Language-wise, Envision treats DP as a first-class citizen, blending it with its relational algebra capabilities. From a supply chain perspective, DP is of prime interest for both performing diverse forecasting tasks and solving varied numerical problems.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Overview

DP emerged in the late 2010s as a descendent of _deep learning_ methods. However, while deep learning emphasizes the design of complex models capable of learning complex functions (hence the 'deep' qualifier), DP is a _programming paradigm_. DP emphasizes the essence of _what it takes_ to implement those (deep learning) models rather than a specific interest for any model in particular. Also, DP represents one more step toward the convergence of two fields _statistical learning_ and _mathematical optimization_, which are increasingly considered as being two sides of the same coin.

For Lokad, DP represents our [6<sup>th</sup> generation of forecasting engine](https://www.lokad.com/forecasting-technology). However, DP is also quite a radical departure from the paradigm that had been driving our machine learning undertakings since the company’s creation back in 2008. Indeed, instead of attempting to deliver a package machine learning framework (as was the case for all the prior generations), DP presents itself as a short series of language keywords. Also, while the interest for DP in the broader community primarily stems from its _learning_ potential, in the specific case of supply chain, we have found that DP equally shines on its capacity to tackle optimization problems - and sometimes to jointly address the two problems at once.

## Linear regression as a first example

Let's consider a simple linear regression problem of the form  $y = ax + b$ where $a$ and $b$ are the two parameters to be learned from a short series of observations while minimizing the MSE (mean squared error). The script below illustrates how such a regression is implemented:

```envision
table T = with
  [| as X, as Y |]
  [| 1, 3.1 |]
  [| 2, 3.9 |]
  [| 3, 5.1 |]
  [| 4, 6.0 |]
 
autodiff T with
  params a auto
  params b auto
  Delta = a * T.X + b - T.Y
  return Delta ^ 2
 
show scalar "Learned" a1c1 with "y ≈ \{a} x + \{b}"
```

In the script above, the `autodiff` keyword introduces the block where _automatic differentiation_ (AD) takes place. We will be revisiting this concept in the section below, but for now, suffice to say this keyword introduces the block where learning/optimization logic takes place. The `params` keyword introduces the _parameters_ that are effectively the output of the process. The `auto` keyword indicates that parameters initilized according to the default rules. Finally, the `return` keyword specifies the _loss value_ that steers the process (or _loss_ in short).

The intermediate variable `Delta` is introduced to illustrate that arbitrary Envision logic can be introduced _after_ the declaration of the parameters and _before_ returning the loss. However, the script above could be rewritten in a slightly more concise manner by inlining the expression of `Delta` with:

```envision
table T = with
  [| as X, as Y |]
  [| 1, 3.1 |]
  [| 2, 3.9 |]
  [| 3, 5.1 |]
  [| 4, 6.0 |]

autodiff T with
  params a auto
  params b auto
  return (a * T.X + b - T.Y)^2

show scalar "Learned" a1c1 with "y ≈ \{a} x + \{b}"
```

DP isn't needed to perform a mean-square linear regression. However, DP shines through its expressiveness. For example, it's straightforward to revisit the example above to learn the 90% upper quantile estimate of the function $y$ by replacing the MSE with a pinball loss:

```envision
table T = with
  [| as X, as Y |]
  [| 1, 3.1 |]
  [| 2, 3.9 |]
  [| 3, 5.1 |]
  [| 4, 6.0 |]

autodiff T with
  params a auto
  params b auto
  Delta = a * T.X + b - T.Y
  return ((if Delta > 0 then 0.1 else 0.9) * abs(Delta))

show scalar "Learned (quantile)" a1c1 with "y ⪅ \{a} x + \{b}"
```

Despite its apparent simplicity, DP can tackle arbitrarily complex problems as long as the problems can be written in the form of a _program_. This allows us to revisit problems that benefit from a closed analytical solution, as it is the case for linear regression under MSE, but also tackle numerous other problems where the closed solution does not exist or simply isn't known to the author of the script.

## General principles

DP boils down to two techniques put together, namely automatic differentiation and stochastic gradient descent. Despite the apparent complexity, DP is remarkably simple when considering all that can be accomplished with these two techniques. A detailed presentation of these two techniques goes beyond the scope of the present document, nevertheless we present some high-level materials that should be sufficient to leverage DP within Envision.

Let's start by introducing a short series of key concepts:

* The _observations_ is the list of data points, which is intended to be used to support the learning/optimization process. For example, each product - associated with its sales history - can be treated as a data point, while the list of all the products would constitute the observations.
* The _program_ is a sequence of instructions that is supposed to provide a correct output for each observation. For example, the program can compute a demand forecast for each product based on its sales history.
* The _parameters_ are floating-point values (i.e. values from $\mathbb{R}$ but with limited precision) which are used by the program, but initially unknown. For example, the program might compute a forecast leveraging a _baseline_ and some _seasonal coefficients_.
* The _loss function_ (or _loss_ for short) quantifies the quality of the solution generated by the program for each observation. By convention, we assume that the lower the loss function, the better. For example, the MSE (mean squared error) can be used as the loss for the forecasts.

The perspective emphasized by DP _assumes_ that a program can be written in such a way that, given the right parameters, it will efficiently execute the learning or optimization task at hand.

_Advanced remark:_ The deep learning community has invented numerous programming patterns that prove particularly effective when composing such programs. Dense layers, convolutional layers, batch normalization, dropout, ..., are but a few of those patterns. However, from a supply chain perspective, the patterns of interest are typically those that are best suited to tackle highly structured relational data. Thus, readers familiar with deep learning might be a bit surprised by the fact that we make little use of these "classic" deep learning patterns. This is not an accident but the consequence of the nature of supply chain problems, which differs considerably from, say, image analysis.

### Automatic differentiation

Differentiation (as in computing the _derivative_ of a function) is of high interest, because any _derivable_ function that is intended as a predictive (or optimization) model of some kind can be "improved" by locally nudging its parameters in a direction that reduces the loss.

There are two widely known methods for computing the derivation of a function: the symbolic method and the numeric method. The symbolic method consists of figuring out the explicit form of the derivative, i.e. if $f(x)=x^2$ then $f^\prime(x)=2x$. However, the symbolic approach is not very practical, because in certain situations the derivative is much more expensive to compute than the original function.

The derivation’s numeric form uses approximation $f^\prime(x) \approx \frac{f(x + \epsilon) - f(x)}{\epsilon}$. However, while this approach is efficient (the compute cost is exactly twice the cost of the original function), it is unfortunately numerically unstable when $\epsilon$ is small, as a division by "almost" zero is involved.

The automatic differentiation (AD) is a third approach which proves to be superior to both the symbolic and the numeric methods. This method is essentially a _program tranformation_ method: through AD, an arbitrary program can be rewritten as _another program_, which computes the derivative. Furthermore, the rewritten form has the same compute complexity as the original program.

The DP paradigm consists of offering the possibility to mark entire sections of arbitrary code as eligible for AD, which is exactly what is being done in Envision via the keyword `autodiff`. The Envision compiler takes care of applying all the necessary transformations to the original script following the AD method.

_Advanced remarks_: Also, despite its apparent technicality, AD is comparatively simpler than many (if not most) compilation methods. However, the main complications do not originate from the AD itself but from the prevention of two undesirable pitfalls associated with "naive" implementation. First, error messages must still relate to the original (i.e. untransformed) script, otherwise those messages are invariably cryptic. Second, while AD ensures that the same _compute_ complexity is achieved, the memory consumption can be significantly larger (known as the _tape_ in AD literature), hence yielding poor performance in practice due to latency effects. Indeed, random accesses for data that fit in the L3 cache are typically an order of magnitude faster than the RAM. Thus, we have adopted a design for Envision that limits the AD expressiveness precisely to avoid _by design_ those performance pitfalls.

### Stochastic gradient descent

The stochastic gradient descent (often abbreviated as SGD) is an iterative method for optimizing an objective function. A dataset is assumed to be given, and the objective function can be applied for each point of the dataset. The objective function depends on a list parameters. The goal is to find the parameter values that minimize the objective function.

Intuitively, the SGD consists of iterating through the dataset by drawing points at random. For each point, the parameter's gradients of the objective function are computed, and parameters are "nudged" a little bit in the direction that minimizes the loss. The direction (i.e. increasing or decreasing the parameter) for the parameter update is defined as the opposite of the gradient.

The SGD is surprisingly capable. While it has its roots in the 1950s, it took nearly 6 decades for the scientific community to realize how powerful this technique actually was. Indeed, some aspects of the SGD are (somewhat) counter-intuitive:

* The SGD does not seek to optimize the "real" objective function, but only a degraded version of this function: its point-wise counterpart. This brings two key benefits. First, the point-wise objective function is much faster to compute. Second, the noise introduced by the point-wise function seems to help the gradient descent (rather than hindering it).
* The direction for the update of the parameters is only "guess-estimated" based on the gradient value. In theory, SGD should only work if the function were displaying smoothness properties. In practice, it works in numerous situations where the gradient is not smooth at all.

Formally, let's introduce $Q$ as the objective function, $w \in \mathbb{R}^k$ the parameters, and $X$ the dataset, the goal is to find $w$ that minimizes:

$$Q(w) = \sum_{x \in X} Q_x(w)$$

where $Q_x$ is the term of the objective function restricted to the point $x$ within the dataset. At each iteration, we draw a random $\hat{x} \in X$ and we update the parameters with:

$$w \leftarrow w - \eta \nabla Q_{\hat{x}} (w)$$

where $\eta > 0$ is the learning rate, a meta-parameter.

In practice, a specific control of the learning rate and its numerical evolution from one iteration to the next greatly improves the SGD’s performance. Under the hood, the Envision runtime is using the Adam algorithm (short for Adaptive Moment Estimation). Discussing the pros and cons of the various algorithms to control the evolution of the learning rate goes beyond the scope of the present document.

## The `autodiff` block

The `autodiff` block is used to introduce a "program" that is first differentiated (via AD) and second optimized (via stochastic gradient descent). Syntax-wise, the `autodiff` block shares multiple similarities with the `each` block, in particular as far as limitations are concerned. Let's revisit a minor variant of the script introduced above.

```envision
table T = with
  [| as X, as Y |]
  [| 1, 3.1 |]
  [| 2, 3.9 |]
  [| 3, 5.1 |]
  [| 4, 6.0 |]

autodiff T with
  params a auto
  params b auto
  absErr = abs(a * T.X + b - T.Y)
  squErr = absErr * absErr
  return (squErr, absoluteError: absErr)

show scalar "Learned" a1c1 with "y ≈ \{a} x + \{b}"
```

The `autodiff` block must end with a `return` statement associated with scalar values. The first - and possibly the sole - value returned is interpreted as the _loss_. The optimization process attempts to minimize this value.

If the `return` statement is associated with a tuple, then the values (beside the first) are interpreted as _metrics_. Those metrics have no influence on the gradient descent, however they benefit from the built-in reporting capabilities associated with `autodiff` blocks. The evolution of the loss and the metrics can be observed via the screen _Dashboard &raquo; Details &raquo; Autodiff Metrics_. Each metric must be named via a prefix introduced by a colon `:` as illustrated above with `absoluteError:`.

<!-- TODO: screenshot, autodiff metrics tab associated to script above -->

The parameters, introduced by the keyword `params`, become regular numeric variables at the end of the `autodiff` block. All parameters must belong to [small tables](/language/relational-algebra/table-sizes/#small-tables).

The logic within an `autodiff` block follows the same design principles as those applicable for the [each blocks](/language/iterations/#each-table-blocks). In particular, the notions of upstream and downstream tables, in regards to the observation table, apply.

However, unlike an `each` block, the `autodiff` block cannot leverage a `scan` option to control the iterations' ordering. Indeed, such a control would not make much sense in regards to the stochastic gradient descent. Also, while both `each` and `autodiff` blocks can be used to return values, their respective semantics differ. This latter point is addressed below.

Finally, an `autodiff` block can use the `Scalar` table (single line) as its observation table. This behavior differs from the `each` block that does not allow iterating over the `Scalar` table. For example, an `autodiff` block using `Scalar` as its observation table can be of interest if the loss function is stochastic.

### Epochs and learning rate

The _epoch count_ and the _learning rate_ are two meta-parameters that impact the stochastic gradient descent.

* The epoch count is a positive integer that indicates the number of full passes to be made over the observation table. When left unspecified, a default value of 10 is used.
* The learning rate is a positive fractional number that represents the initial scaling factor used for the parameter update (cf. above). When left unspecified, a default value of 0.01 is used.

The script below illustrates how these two meta-parameters can be used:

```envision
table T = with
  [| as X, as Y |]
  [| 1, 3.1 |]
  [| 2, 3.9 |]
  [| 3, 5.1 |]
  [| 4, 6.0 |]

autodiff T epochs:10 learningRate:0.01 with
  params a auto
  params b auto
  return abs(a * T.X + b - T.Y)

show scalar "Learned" a1c1 with "y ≈ \{a} x + \{b}"
```

As a rule of thumb, it's good to keep the number of epochs reasonably low in regards to the actual convergence. Indeed, the compute resources associated with an `autodiff` block are strictly linear in the number of epochs. Also, keep in mind that there is no point in achieving a 0.01% convergence on a forecasting metric if the forecast is only expected to be about 10% accurate.

The learning rate is usually best left untouched. The convergence’s performance rarely depends on precise initial learning rate values. When this is the case, it usually hints at design problems for the loss function and its parameters. Control over the learning rate can be handy however to temporally "duct tape" numerical instabilities while the design of the loss function is still a work-in-progress.

### Parameter's initialization and bounds

By default, parameters are initialized as random deviates drawn from a normal distribution of mean 1.0 and of standard deviation 0.1. The mean and standard deviation of the normal distribution can be controlled by passing two arguments to the `auto` keyword as illustrated by:

```envision
table T = with
  [| as X, as Y |]
  [| 1, 3.1 |]
  [| 2, 3.9 |]
  [| 3, 5.1 |]
  [| 4, 6.0 |]

autodiff T with
  params a auto(1.0, 0.1) // like the 'auto' without arguments
  params b auto(2.5, 0.01)
  return abs(a * T.X + b - T.Y)

show scalar "Learned" a1c1 with "y ≈ \{a} x + \{b}"
```

In the above script, the parameter `a` is explicitely initialized a mean of `1.0` and a standard deviation of `0.1`. Those two values are the defaults when `auto` is used without arguments. The parameter `b` is initialized using values which do not match the defaults of `auto`.

However, it is possible to specify an explicit initialization as illustrated in the script below:

```envision
table T = with
  [| as X, as Y |]
  [| 1, 3.1 |]
  [| 2, 3.9 |]
  [| 3, 5.1 |]
  [| 4, 6.0 |]

a = 1.25
b = (a + 1) ^ 0.75

autodiff T with
  params a
  params b 
  return abs(a * T.X + b - T.Y)

show scalar "Learned" a1c1 with "y ≈ \{a} x + \{b}"
```

In the script above, the parameter initialization is done above the `autodiff` block. Thus, the keyword `auto` is not needed, neither for `a` nor `b`.

Explicit parameter initialization can be of interest in order to inject prior knowledge into the resolution of the optimization problem.

It is also possible to control the range of acceptable values of a parameter:

```envision
table T = with
  [| as X, as Y |]
  [| 1, 3.1 |]
  [| 2, 3.9 |]
  [| 3, 5.1 |]
  [| 4, 6.0 |]

autodiff T with
  params a in [1 ..] auto(1.5, 0.1)
  params b in [.. 1.5] auto
  return abs(a * T.X + b - T.Y)

show scalar "Learned" a1c1 with "y ≈ \{a} x + \{b}"
```

In the above script, the parameter `a` is only allowed to vary within the range $[1,+\infty[$ (as only the right bound is specified), while the parameter `b` is restricted to the range $]-\infty, 1.5]$ (as only the left bound is specified).

The valid value range is introduced by the keyword `in`, which is expected to be followed by a pair of square brackets `[]`. The delimiter `..` is used to introduce the left and right bounds respectively. It is acceptable to omit one (but not both) of the bounds within the brackets.

When a range is specified for a parameter, the runtime truncates the evolution of the parameter so that it always remains within the specified range. Whenever a bound is hit, after a step of gradient descent, not only is the parameter value truncated but the momentum values are also reset to zero.

When a range is specified along with `auto`, the boundaries must be at least 3 standard deviation away from the mean of the normal distribution. This behavior is intended to avoid the truncation accidentally eliminating the intended random initialization of the parameters.

Specifying a range is of great interest whenever parameters have a semantic interpretation that dictates that their values remain within specific ranges. For example, a seasonality coefficient should remain non-negative. In particular, bounds tend to be more manageable than the introduction of _ad hoc_ numerical penalties within the loss itself, in order to steer the gradient descent away from unacceptable parameter values.

It is also possible, for a given parameter, to both specify an initialization and a range.

```envision
table T = with
  [| as X, as Y |]
  [| 1, 3.1 |]
  [| 2, 3.9 |]
  [| 3, 5.1 |]
  [| 4, 6.0 |]

a = 1.25

autodiff T with
  params a in [1 .. 3]
  params b in [ .. 1.5] auto
  return abs(a * T.X + b - T.Y)

show scalar "Learned" a1c1 with "y ≈ \{a} x + \{b}"
```

In the script above, the parameter `a` is initialized with the value 1.25. The evolution of the parameter is then restricted to the range $[1, 3]$.

<!-- 

### Collecting the loss and the metrics

TODO: the syntax is only halfway implemented, the example below works but
the table 'M' isn't properly populated.

```envision
table T = with
  [| as X, as Y |]
  [| 1, 3.1 |]
  [| 2, 3.9 |]
  [| 3, 5.1 |]
  [| 4, 6.0 |]

table M = autodiff T with
  params a auto
  params b auto
  return abs(a * T.X + b - T.Y)

show scalar "Learned" a1c1 with "y ≈ \{a} x + \{b}"
```

-->

## Non-scalar parameters

DP is not limited to scalar parameters. In this section, we propose a more complex example that hints at what can be done with vector parameters. Intuitively, we propose below a naive weekly demand model defined as the multiplication of two factors: the _store_ factor and the _product_ factor.

<!-- TODO: example to be simplified further by using 'W' as the observation table directly:
https://lokad.atlassian.net/browse/LK-8321  -->

```envision
keep span date = [date(2020, 1, 1) .. date(2020, 3, 5)]

table Orders = with
  [| as Store, as Product, as MyDate, as Quantity |]
  [| "paris",  "cap", date(2020, 1, 5),  1 |]
  [| "london", "cap", date(2020, 1, 2),  2 |]
  [| "london", "cap", date(2020, 1, 1),  2 |]
  [| "paris",  "cap", date(2020, 2, 4),  1 |]
  [| "paris",  "hat", date(2020, 1, 6),  2 |]
  [| "paris",  "hat", date(2020, 1, 18), 2 |]
  [| "london", "hat", date(2020, 2, 1),  2 |]
  [| "london", "hat", date(2020, 2, 3),  2 |]

keep where Orders.date = Orders.MyDate

table Stores[store] = by Orders.Store
table Products[product] = by Orders.Product
table Skus = by [Orders.Store, Orders.Product]

table W = cross(Skus, Week)
W.store = Skus.store
W.product = Skus.product
W.Qty = sum(Orders.Quantity)

table Sales = by [W.store, W.product, week]
Sales.Qty = sum(W.Qty)

autodiff Sales with
  params Stores.A in [0.1 ..] auto
  params Products.B in [0.1 ..] auto

  Demand = Stores.A * Products.B
  Delta = (Demand - Sales.Qty)

  return (Delta * Delta)

show table "Store factors" a1b3 with store, Stores.A
show table "Product factors" c1d3 with product, Products.B
```

The above script is extensively leveraging not only the differentiable programming capabilities of Envision, but also its relational algebra. We have:

* Line 1: The `keep span` introduces the `date` dimension. The `Day` table is implicitly defined.
* Line 14: The table `Orders` now embarks `date` as a foreign dimension.
* Lines 16-17: Two tables `Stores` and `Products` are defined, as well as their respective dimensions `store` and `product`. The table `Orders` gains those two dimensions as foreign dimensions.
* Line 18: The table `Skus` is defined from the `Orders` table. This table inherits the two foreign dimensions of the table `Orders`.
* Line 20: The table `W` is defined as a cross table (Cartesian product) between `Skus` and `Week`.
* Lines 21-22: The table `Week` gains two foreign dimensions, respectively `store` and `product`, imported via its composing table `Skus`.
* Lines 29-30: Two parameters `Stores.A` and `Products.B` are defined. Those parameters are vectors, with one value per line of the respective tables `Stores` and `Products`.
* Line 32: For every line of the `Sales` table there is exactly one matching line in the `Stores` table (resp. in the `Products` table). Hence, both `Stores.A` and `Products.B` are scalars in this line.
* Lines 37-38: The learned parameters are put on display.

This model of the demand is simplistic and primarily intended to demonstrate the syntax of `autodiff`. Nevertheless, the differentiable programming paradigm makes it straightforward to consider more elaborate models.

## Dependent parameters
<!-- TODO: screenshot of the scatter plot below -->
Parameter sharing is a powerful mechanism to express a problem’s structure. However, Envision restricts arbitrary lookups over vectors of parameters, as those lookups would most likely be computationally inefficient. Instead, Envision introduces the notion of _dependent_, which is a more controlled approach to lookups over a parameter’s vectors.

In order to illustrate this mechanism, let’s consider a simple planar point placement problem where each point should be at the same distance from the origin and where each point should be at the same distance from its predecessor and successor. The resolution of this problem can be written as:

```envision
n = 50
table T[t] = extend.range(n)
T.t1 = t
T.t2 = same(t) by ((T.N mod n) + 1) at T.N
c = (6.283 / (n - 1))^2

autodiff T epochs: 1000 with
  params T.X abstract auto(0, 0.1)
  params T.Y abstract auto(0, 0.1)
  params x1 = T.X[T.t1]
  params y1 = T.Y[T.t1]
  params x2 = T.X[T.t2]
  params y2 = T.Y[T.t2]
  return (x1^2 + y1^2 - 1)^2 + ((x1 - x2)^2 + (y1 - y2)^2 - c)^2

show scatter "Solution" a1c6 with T.X, T.Y
```

In the above script, the parameters `T.X` and `T.Y` are declared as `abstract`. They won’t be directly used in the `autodiff` blocks. Instead, a series of dependent parameters, namely `x1`, `y1`, `x2` and `y2`, are introduced based on lookups over `T.X` and `T.Y`. Those dependent parameters are scalars. They contribute to the loss function that reflects the problem statement of interest.

The keyword `abstract` can be applied to any parameter. In the above script, the parameters did belong to the observation table, but the same mechanism would work for any other table. The keyword indicates that the parameter vector “abstracted away” from the AD. Dependent parameters are introduced with the equality sign `=` and an expression, on the right side, containing a lookup over an abstract parameter.

Performance-wise, the SGD overhead is proportional to the count of values lying in the dependent parameters themselves. In the script above, it means that 4 parameter values are updated for each SGD step. In contrast, the direct (and naive) use of the full parameter vectors would have results in 2 * 50 = 100 parameter values to be updated for each SGD step.

### Vector dependent parameters

Dependent parameters can be vectors, not just scalars. Indeed, if a parameter is defined over a cross table then a lookup over the _second_ dimension of the cross table returns a vector of dependent parameters. Let's revisit the script of the previous section, packing the two coordinates X and Y with a cross table:

```envision
n = 50
table T[t] = extend.range(n)
T.t1 = t
T.t2 = same(t) by ((T.N mod n) + 1) at T.N
c = (6.283 / (n - 1))^2
 
table enum D[d] = "x", "y"
table C = cross(T, D)

autodiff T epochs: 1000 with
  params C.XY abstract auto(0, 0.1)
  params D.XY1 = C.XY[T.t1]
  params D.XY2 = C.XY[T.t2]
  return (sum(D.XY1^2) - 1)^2 + (sum((D.XY1 - D.XY2)^2) - c)^2
 
show scatter "Solution" a1c6 with C.XY[t: t, d: "x"], C.XY[t: t, d: "y"]
```

In the script above, the enum table `D` is defined with 2 lines, reflecting the two coordinates X and Y. The table `C` is packing the two coordinates X and Y for every line of `T`. The `autodiff` block keeps the same semantic. However, there are only two dependent parameters (there were 4 previously) `D.XY1` and `D.XY2` which happen to be vectors. The `scatter` tile uses labeled lookups to extract the two coordinates X and Y from `C` for every line of `T`.

## Differentiable user-defined functions
<!-- TODO: screenshot of the scatter plot below -->
User-defined functions may be eligible for AD as long as all their inner operations happen to also be eligible for AD. Let’s revisit the script introduced in the previous section:

```envision
n = 50
table T[t] = extend.range(n)
T.t1 = t
T.t2 = same(t) by ((T.N mod n) + 1) at T.N
c = (6.283 / (n - 1))^2

def autodiff pure dist2(x1 : number, y1 : number, x2 : number, y2 : number) with
  return (x1 - x2)^2 + (y1 - y2)^2

autodiff T epochs: 1000 with
  params T.X abstract auto(0, 0.1)
  params T.Y abstract auto(0, 0.1)
  params x1 = T.X[T.t1]
  params y1 = T.Y[T.t1]
  params x2 = T.X[T.t2]
  params y2 = T.Y[T.t2]
  return (dist2(x1, y1, 0, 0) - 1)^2 + (dist2(x1, y1, x2, y2) - c)^2

show scatter "Solution" a1c6 with T.X, T.Y
```

In the above script, a user-defined function named `dist2` is introduced. The keyword `autodiff`, which precedes the `pure` keyword, indicates that this function can be automatically differentiated. The loss function makes two calls to this `dist2` function.

Within an `autodiff` block, any call to a user-defined function requires the function to be marked with the `autodiff` keyword. However, a user-defined function marked with `autodiff`can also be called outside `autodiff` blocks.

If the user-defined function marked with `autodiff` contains elements that are not compatible with AD (e.g. a call to the function `parseNumber`), then the compilation fails with a hint at the problem.

## Illustration: Probabilistic modeling

AD is well-suited for probabilistic modeling. In particular, both the regression perspective and the generation perspective are eligible. The following script illustrates the two perspectives applied to a normal distribution.

```envision
table T = extend.range(1000)
mu0 = 1
sigma0 = 2

// learn a parametric distribution from observations
T.X = random.normal(mu0 into T, sigma0)
autodiff T with
  params mu auto
  params sigma in [0.001 ..] auto
  return -loglikelihood.normal(mu, sigma, T.X)

show summary "Regressed Distribution" a1b1 with mu, sigma // 1.03, 1.97

// learn a parametric generator from moments
autodiff T with
  params mu auto
  params sigma in [0.001 ..] auto

  x1 = random.normal(mu, sigma)
  x2 = random.normal(mu, sigma)

  return (x1 - mu0)^2 + (((x1 - x2)/2)^2 - log(2 * 3.14159) * sigma0^2)^2

show summary "Regressed Generator" a2b2 with mu, sigma // 0.94, 2.10
```

The above script is split into two blocks: first learning a parametric distribution, second learning a parametric generator.

In the first block, the maximization of the likelihood (or rather log-likelihood) yields the parameters `mu` and `sigma` that fit the observations collected in `T.X`. The loss function is _minus_ the log-likelihood as `autodiff` minimizes the loss by convention. The parameter `sigma` is constrained to be greater than `0.001` as the log-likelihood function doesn't allow negative standard deviations.

In the second block, the minimization of a metric, which characterizes the distribution of the differences of deviates sampled from two normal distributions, yields the parameters `mu` and `sigma`. This case can be seen as the _dual_ of the previous one. The regression is operated _through_ the calls to `random.normal`, i.e. we are learning the parameters of a generator.

From an AD perspective, it is notable that `random.normal` is not only differentiable, but that its gradients are non-zero.

_Advanced remark:_ In the literature, the function `random.normal` is known as one of the popular stochastic nodes. The AD of those nodes is of special interest for variational autoencoders which are beyond the scope of this document.

## Illustration: Clustering

AD is suitable for clustering. The following scripts illustrates a simple k-means problem with points distributed over the unit circle.

```envision
table T[t] = extend.range(50) // points
table enum D[d] = "x", "y"
table TD = cross(T, D)
TD.XY = random.uniform(-1 into TD, 1)
TD.XY = TD.XY / sqrt(sum(TD.XY^2) into T) // unit circle

table C[c] = extend.range(10) // centroids
table CD = cross(C, D)
CD.XY = random.uniform(-0.5 into CD, 0.5) // random init

table TC = cross(T, C)

autodiff T epochs:100 with // actual clustering
  params CD.XY
  params TC.W in [0.001 .. 1] auto(0.1, 0.01)
  C.W = TC.W / sum(TC.W into C) by 1 // normalize affinities
  D.T_XY = TD.XY
  C.d2 = sqrt(sum((D.T_XY - CD.XY)^2))
  return sum(C.W * C.d2)

// Display points and centroids
T.X = TD.XY[d:"x"]
T.Y = TD.XY[d:"y"]
C.X = CD.XY[d:"x"]
C.Y = CD.XY[d:"y"]

table U = with
  [| T.X as X, T.Y as Y, true as IsPoint |]
  [| C.X,      C.Y,      false           |]

U.Color = if U.IsPoint then "blue" else "red"
show scatter "Points (blue) and Cendroids (red)" a1d8 with 
  U.X 
  U.Y { color: #[U.Color] }
```

In the above script, the vector `CD.XY` contains the centroids while the vector `TC.W` contains the affinity between points and centroids. The use of the cross tables `TD`, `CD` and `TC` keeps the logic tidy. The table `U` gathers both points and centroids in order to provide a single view through a scatter plot.

The above script can be run alternatively with 1, 10 and 100 epochs in order to visualize the gradual displacement of the centroids toward the unit circle.

## Illustration: Cluster-based cyclicities

AD is suitable to learn cyclities as observed in demand and other phenomenons. The seasonality profiles and day-of-week profiles can be learned with a clustering approach. This approach does not require prior knowledge on relevant groupings for the profiles.

```envision
keep span date = [date(2017, 1, 1) .. date(2022, 6, 13)]
table Skus = extend.range(100)

table SkusDay = cross(Skus, Day)
table SkusWeek = cross(Skus, Week)

// BEGIN: mock demand data
SkusDay.MockS = ((weekNum(date) + Skus.N) mod 10) * ((date + Skus.N) mod 7 + 1) / 20
SkusDay.Observed = random.poisson(SkusDay.MockS into SkusDay)
SkusWeek.Observed = sum(SkusDay.Observed)
// END: mock demand data

table WeekOfYear[woy] max 52 = by (weekNum(week) mod 52)
table DayOfWeek[dow] max 7 = by (date mod 7)

table C = extend.range(/* cyclical patterns */ 10)
table CWoY small = cross(C, WeekOfYear) // week-of-year cyclicities.
table CDoW small = cross(C, DayOfWeek)  // Weekly cyclicities
table SkusC small = cross(Skus, C)      // Affinities to cyclicities

table CWeek small = cross(C, Week)
CWeek.woy = woy
table CDay small = cross(C, Day)
CDay.dow = dow

autodiff Skus epochs:1500 learningRate:0.01 with
  params SkusC.AffWoY in [0.01..] auto  // Affinities to Week-of-Year profiles.
  params SkusC.AffDoW in [0.01 ..] auto // Affitinities to Day-of-Week profiles.
  params CWoY.X in [0.01..] auto        // Week-of-year profiles
  params CDoW.X in [0.01 ..] auto       // Day-of-Week profiles
  params Skus.Level in [0.01..] auto // SKU daily level

  C.AffWoY = SkusC.AffWoY / (sum(SkusC.AffWoY) by 1) // normalize
  C.AffDoW = SkusC.AffDoW / (sum(SkusC.AffDoW) by 1) // normalize
  CWoY.X = 52 * CWoY.X / (sum(CWoY.X) by C.N) // normalize
  CDoW.X = 7 * CDoW.X / (sum(CDoW.X) by C.N) // normalize

  CWeek.Demand = 7 * Skus.Level * CWoY.X
  CWeek.Loss = (CWeek.Demand - SkusWeek.Observed)^2

  CWeek.Level = Skus.Level * CWoY.X * SkusC.AffWoY
  Day.Level = sum(CWeek.Level)/7 into Week

  CDay.Demand = (Day.Level into CDay) * CDoW.X
  CDay.Loss = (CDay.Demand - SkusDay.Observed)^2

  return sum(CWeek.Loss * C.AffWoY) + sum(CDay.Loss * C.AffDoW)

SkusC.AffToY = SkusC.AffWoY / (sum(SkusC.AffWoY) by Skus.N)
SkusC.AffToD = SkusC.AffDoW / (sum(SkusC.AffDoW) by Skus.N)
CWoY.X = 52 * CWoY.X / (sum(CWoY.X) by C.N)
CDoW.X = 7 * CDoW.X / (sum(CDoW.X) by C.N)

show table "Skus" a1b10 with SkusC.AffToY, SkusC.AffToD, Skus.N, C.N, Skus.Level
show table "Week of Year" c1d10 with C.N, woy, CWoY.X
show table "Day of Week" e1f10 with C.N, dow, CDoW.X
show table "SKUDay" with SkusDay.MockS, date
```
{{<skiptest this takes 4.5min to run.>}}
