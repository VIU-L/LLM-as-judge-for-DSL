+++
title = "autodiff"
+++

## autodiff, keyword, block

The `autodiff` keyword introduces a block intended for a stochastic gradient descent. The logic within the `autodiff` block is automatically differentiated. The keyword is followed by the name of the observation table.

```envision
autodiff Scalar epochs: 500 learningRate: 0.1 with
  params a auto
  s = a * a
  return s

show scalar "" with a // 0.00
```

The option `epochs` is optional; its default value is 10.

The option `learningRate` is optional; its default value is 0.01.

### The `parallel` mode

The execution of the `autodiff` block can be automatically parallelized. This execution mode is intended for larger datasets. This parallelization typically incurs a modest decrease of convergence speed - counted in epochs - in exchange for a faster wall-clock execution.

```envision
autodiff Scalar epochs: 500 learningRate: 0.1 mode: "parallel" with
  params a auto
  s = a * a
  return s

show scalar "" with a // 0.00
```

In the script above, the `mode` option is set to `parallel`.

### The `batch` mode

For datasets with high dissimilarities, batch processing may stabilize the learning process. It updates the model's parameters using a batch of observations instead of an individual observation. This method may require more iterations to converge but is useful when some observations differ significantly from the others.

```envision
table Obs = extend.range(10000)

lambda = 10
Obs.Y = random.poisson(lambda into Obs)

autodiff Obs batch:100 with
  params lambdaEstimation auto(9.5 ,0)
  return -loglikelihood.poisson(lambdaEstimation, Obs.Y)
 
show summary "Regressed Poisson distribution (batch)" a1b1 with lambdaEstimation // 10.02


autodiff Obs with
  params lambdaEstimation auto(9.5 ,0)

  return -loglikelihood.poisson(lambdaEstimation, Obs.Y)
 
show summary "Regressed Poisson distribution (no batch)" a2b2 with lambdaEstimation // 9.90
```

In the script above, we estimate the poisson parameter. The autodiff block with `batch` mode is more accurate than the classical one.

### The `gradient` mode

The `gradient` mode is intended to debug a strange behavior in an autodiff block. It returns the gradient of the parameters (not the update!) during one and only one epoch. When a parameter is utilized multiple times within an epoch, such as when it originates from a Scalar/Upstream table, the gradient is accumulated across these occurrences, and the sum of the gradients is returned.

```envision
autodiff Scalar mode:"gradient" with
  params X auto(1,0)

  Loss = X * X
  return Loss

show scalar "d(Loss)/d(X) = X * X" with X
```

In the script above, the parameter is not updated but stores the computed gradient through the one and only one "epoch".

### The `validation` mode
  
The `validation` mode is intended to monitor overfitting. It splits the dataset into two parts: training and validation. The training data is used as usual, while the validation data is not used for updating the block's parameters. Validation can be applied only if parameters are located in upstream, full, or upstream-cross tables. If a parameter is in the observation table, the parameter lines in the validation set will not be updated. Validation curves are displayed in the autodiff metrics.

```envision
table Observations = extend.range(50)

Observations.Cat = random.integer(5)
Observations.Y = Observations.Cat + random.normal(0, 0.1)

table Categories[Cat] = by Observations.Cat

Observations.IsTest = random.binomial(0.5 into Observations)

// The validation option expects either
//      - a scalar number between 0 and 1
//      - a boolean vector in the observation table wich indicates
//        if the observation is concerned by the validation set

autodiff Observations validation:Observations.IsTest  with
  params Categories.Alpha auto
  Loss = (Categories.Alpha - Observations.Y)^2
  return Loss

show table "Validation from boolean vector" a1b2 with Categories.Alpha

autodiff Observations validation:0.5 with
  params Categories.Alpha auto
  Loss = (Categories.Alpha - Observations.Y)^2
  return Loss

show table "Validation from scalar number" c1d2 with Categories.Alpha
```

The validation curves can be found in the autodiff metrics of the run.

## autodiff, keyword, pure function option

The `autodiff` keyword indicates that the pure function can be executed inside an `autodiff` block

```envision
def autodiff pure mySquare(x: number) with 
  return x * x

autodiff Scalar epochs: 500 with
  params a auto
  return mySquare(a)

show scalar "" with a // 0.00
```

In the present reference documentation, pure functions that are part of the Envision standard library and that can be executed inside an `autodiff` block are marked as `autodiff`.
