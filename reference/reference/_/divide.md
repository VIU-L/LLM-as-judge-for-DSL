+++
title = "(/) divide operator"
+++

## (number / number) 🡒 number, const

The division of two numbers. Any division by zero causes a error that interupt the execution of the script.

```envision
x = 3 / 4
show scalar "" with x
```

## (number /. number) 🡒 number, const autodiff

The operation `a /. b` where `a` and `b` are numbers is defined by `a / (if b == 0 then 1 else b)`. This is the "passthrough" division of two numbers.

```envision
x = 3 /. 0
show scalar "" with x
```
