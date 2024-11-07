+++
title = "noGrad"
+++

## noGrad(a: number) 🡒 number, const autodiff pure function

Returns the specified number but without propagating gradient through this usage.

```envision
autodiff Scalar epochs:100 with
  params A auto(1,0)  // A starts at '1.0'
  Loss = A - noGrad(A)
  return Loss

show scalar "A" with A // A ends at '0.0'
```

The loss of this `autodiff` block is equal to zero, but the gradient of the parameter `A` is equal to `1`.

## See also

* [Differentiable Programming](../../../language/differentiable-programming/)
