+++
title = "regularizationTerm"
+++

## regularizationTerm(penalty: number, loss : number, alpha : number) 🡒 number, const autodiff pure function

Returns a penalization term constructed from the number `penalty` that is scaled as a fraction `alpha` of the original `loss`.

When training a model, it is often desirable to impose additional constraints on the learned parameters that cannot be directly encoded with bounds. To achieve this, additional terms are introduced in the loss function to penalize undesired behaviors. These additional terms are known as regularization terms. This function is intended to serve as a baseline to deal with regularization terms in autodiff blocks. This is not restrictive and other regularization functions can be implemented.

For small `penalty` values, it reduces to:

$$\text{regularizationTerm}(penalty, loss, \alpha) = \alpha \times \text{noGrad}(loss) \times \tanh(penalty) $$

A different behavior is implemented for larger `penalty` values due to tanh gradient tending towards $0$.

Scalar `loss` can be safely used in the function as it is used through the [noGrad](../../mno/nograd/) function in it.

Scalar `alpha` represents the importance of the penalty compared to the `loss`. `alpha = 0.1` means that penalty will be responsible for 10% of each parameter update.

### Example: in-circle upper-right coordinates

As an illustrative example, consider the task of finding coordinates that are positioned in the upper-right quadrant while still remaining within the unit circle.

In cartesian coordinates it is not feaseable to force it to be in the unit circle with bounds. `regularizationTerm` is used to do so, while $\frac{1}{(X+Y)^2}$ is used to represent the objective of being in the upper-right quadrant.

```envision
autodiff Scalar learningRate:0.1 epochs:100 with
  params X in [0.01 ..] auto(0.35, 0)
  params Y in [0.01 ..] auto(0.25, 0)

  Loss = 1 / (X+Y)^2
  Radius = (X^2 + Y^2)^2
  Penalty = if Radius > 1 then Radius else 0
  Regularization = regularizationTerm(Penalty, Loss, 3.0)
  return (Loss + Regularization; X:X, Y:Y)

show table "Coordinates obtained with regularization" a1d3 with
  Scalar.X as "X"
  Scalar.Y as "Y"
  X^2 + Y^2 as "r^2"
```

`alpha` is set to 300% since remaining within the unit circle is not merely a desired behavior but a stringent condition that must be met.

### Annex: `regularizationTerm` re-implemented

The function `regularizationTerm` is equivalent as:

```envision
def autodiff pure regularizationTerm2(penalty: number, loss : number, alpha : number) with

  /// The penalty is scaled between 0 and 1 with a gradient that does not converge to 0.
  /// If the penalty is under 1.8 (magic number, after this value, tanh gradient is too
  /// small), then uses tanh.
  /// After this limit one uses the rest of the floor function.
  /// Note that noGrad is used as the floor's gradient is hand coded as 1.

  /// To make computation faster:
  /// 1 - tanh(1.8)^2 = 0.10355837
  /// tanh(1.8) = 0.94680601
  
  scaledPenalty = if penalty < 1.8 then tanh(penalty) else 0.10355837*(penalty - floor(noGrad(penalty)/1.8) * 1.8) + 0.94680601
  /// The scaled penalty (between 0 and 1) is then scaled by the original loss, 
  /// used without impacting gradient.
  return alpha * noGrad(loss) * scaledPenalty
```

## See also

* [Differentiable Programming](../../../language/differentiable-programming/)
* [autodiff](../../abc/autodiff/)
* [noGrad](../../mno/nograd/)
