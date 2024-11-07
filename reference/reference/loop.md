+++
title = "loop"
+++

The `loop` keyword offers a mechanism to repeat a short series of Envision operations. The maximal number of iterations is 10. This low maximum is intentional as arbitrary loops introduce problems that are better solved through the other constructs of the Envision language.

See [iterating with 'loop'](/language/iterations/loop/) for detailed usage documentation. 

## loop (n : number), code block

The `loop` keyword takes a single argument which must be an integer constant between 1 and 10 (inclusive).

```envision
a = 1
loop 3
  b = a + 1
  a = 2 * b
show summary "" with a, b // 22, 11
```

## loop (n : number) in (low : number) .. (high : number), code block

The `loop` keyword defines an iteration variable over a range of integer values. The boundaries are inclusive, and must contain between 1 and 10 values. 

```envision
s = 0
loop n in 11 .. 15
  s = s + n
show summary "" with s // 65
```

## loop (n : number) in sequence, code block

The `loop` keyword defines an iteration variable over an explicit list of values.

```envision
msg = ""
loop n in ("h", "e", "l", "l", "o")
  msg = concat(msg, n)
show summary "" with msg // 'hello'
```
