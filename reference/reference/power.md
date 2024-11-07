+++
title = "(^) power operator"
+++

## (number ^ number) 🡒 number, const autodiff

The power operation between two numbers. If the first number is negative, then the second number must be an integer, or the operation fails.

```envision
show summary "" a1d1 with
  2 ^ 2
  2 ^ -2
  -2 ^ 3
  -2 ^ -3
```

## (ranvar ^ number) 🡒 ranvar

The expression `(r ^ n)` with `r` a ranvar and `n` a number is defined by `(r ^ dirac(n))`.

Example:

```envision
show scalar "" a1c2 with poisson(5) ^ 2
```

## (ranvar ^ ranvar) 🡒 ranvar

The convolution power between ranvars.

```envision
show scalar "" a1c2 with poisson(5) ^ poisson(2)
```

### Annex: convolution power

The convolution power is a relatively advanced mathematical operation. In supply chain, convolution power can be used to scale probabilistic demand forecasts up or down. Convolution power offers the possibility to perform linear-like numeric adjustments on probabilistic forecasts. Furthermore, convolution power can be interpreted as the probabilistic counterpart of the linear adjustments performed on "classic" forecasts - i.e. periodic forecasts regressed against the mean or the median.  

#### Motivation

Probabilistic demand forecasts are particularly suitable for optimizing decisions while taking supply chain risks into account. However, unlike classic forecasts where the demand is expressed as a definite quantity associated with a specific period of time, probabilistic forecasts involve distributions of probabilities (referred to as _ranvars_, in the following).  
  
While ranvars provide more insights about the future compared to single-point indicators, they are more complex to manipulate. Such manipulations may be required to reflect market evolutions that cannot be inferred from historical data. The convolution power is a mathematical operation that allows to scale a ranvar of probabilities in a pseudo-linear fashion.  
  
For example, if a retailer knows that each promotion will bring a 100% increase in sales, then, all it takes to adjust a classic demand forecast - which ignores promotions - is to multiply the original number by 2. In the case of a probabilistic forecast ignoring promotions, it is not possible to multiply the ranvar by 2 in the naive sense because the sum of the ranvars needs to remain equal to 1.  

#### Formal definition

In mathematics, the convolution power is the $n$-fold iteration of the convolution with itself. Thus, if $R$ is a function $\mathbb{Z} \to \mathbb{R}$ and if $n$ is a non-negative integer, the convolution power is defined by:

$$ R^{*n} = \underbrace{R * R * R * \cdots * R * R}_n,\quad R^{*0}=\delta_0 $$

where $*$ denotes the convolution operation and $\delta_0$ is the Dirac delta ranvar. The variable $n$ is referred to as the _exponent_.  
  
If $R$ is the ranvar associated with the discrete random variable $X$ with $R(k)=\mathbf{P}[X=k]$, then the convolution power $R^{*n}$ can be interpreted as the ranvar of the sum of $n$ independent random variables all having the same individual ranvar $R$:

<div>$$
X^{*n} = \underbrace{X + X + X + \cdots + X + X}_n
$$</div>

#### Fractional exponents

Convolution power, as introduced in the previous section, is defined for non-negative integers used as exponents. However, from a practical perspective, it is desirable to have fractional exponents. For example, if the promotional uplift is only 50%, then, we would seek to apply convolution power with $n=1.5$ instead. Here, we generalize the convolution power to arbitrary positive real numbers to be used as exponents.  

We define the convolution power by a number $1 / q$ as the inverse of the convolution power by $q$.
For example, let us consider the convolution power ${R}^{*1/{2}}$: the solution $R^\prime$ to the equation $R^\prime = {R}^{*1/{2}}$, if it exists, satisfies the equation $R = {R^\prime}^{*2}$.

However, a given ranvar $R$ may not have roots for any $1/q$ (a root being the ranvar $R^\prime$ so that ${R^\prime}^{*q} = R$). In fact, in the set of discrete probability ranvars, only Poisson and negative binomial ranvars have roots for any value of $1/q$ (see [infinite divisibility](https://en.wikipedia.org/wiki/Infinite_divisibility_(probability))). This is why our approach to compute the fractional part of the convolution power is more “common-sense” based than mathematically grounded, since, again, there is most of the time no defined solution.

The approach we choose is a mix of two approximations.
The first one is the approximation of $R^{*1/q}$ with $\text{transform}(R,1/q)$. This Envision operation squeezes the ranvar by a factor $1/q$, while conserving its shape. However, it does not scale well for small fractional values, due to the fact that `transform` itself is not properly mathematically defined for discrete ranvars.
On the other hand, we can approximate $R^{*1/q}$ with a negative binomial ranvar of parameters $(r \times 1/q, p)$. This is the $1/q$ root of the [negative binomial](https://en.wikipedia.org/wiki/Negative_binomial_distribution) ranvar of parameters $(r, p)$, where $r$ and $p$ are tuned so that the mean and variance and of $\text{negativeBinomial}(r,p)$ are equal to the mean and variance of the ranvar $R$. This approximation is robust for small $1/q$ values, but when a gets close to 1, it tends not to reproduce the shape of $R$.
To obtain the final result, these two approximations are mixed by taking their convolution, with weights $(1 - 1/q)$ for the transform and $1/q$ for the negative binomial:

$$R^{*1/q} = \text{transform}(R, 1/q\times (1-1/q)) * \text{negativeBinomial}(r\times 1/q^2,p)$$

In this way we ensure that we will tend to approximate the solution with $\text{transform}$ when $1/q$ is closer to 1, by a negative binomial when $1/q$ is closer to 0, and by a mix of the two solutions in between.

This allows us to define the convolution power for any rational number $p/q$ and, following on from the density of rational numbers in the real line, to any real number.

#### Illustration: aerospace spare parts

Let's consider an airline company that operates a homogeneous fleet of 100 aircrafts. The company needs to optimize its inventory of APUs (Auxiliary Power Units) which happen to be an expensive repairable component required by the aircraft. The demand for APUs has been forecast for the horizon of interest as a probabilistic demand forecast $D$  
  
Now, this company has the opportunity to buy a small competitor operating 5 aircrafts that are homogeneous to our company's own fleet. Through this competitor acquisition, the company gains extra aircrafts and extra passengers. If we assume that all aircrafts are statistically independent in their need for APUs, and if we assume that the competitor's aircrafts have needs similar to those of the acquiring company, then, the total demand for APUs for the merged entity can be revised as $D^{*\frac{100 + 5}{100}}=D^{*1.05}$.  
  
#### References

* [Convolution](https://en.wikipedia.org/wiki/Convolution), Wikipedia
* [Convolution power](https://en.wikipedia.org/wiki/Convolution_power), Wikipedia
* [Negative binomial](https://en.wikipedia.org/wiki/Negative_binomial_distribution), Wikipedia
* [Infinite divisibility](https://en.wikipedia.org/wiki/Infinite_divisibility_(probability)), Wikipedia
