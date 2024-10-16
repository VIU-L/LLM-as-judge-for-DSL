+++
title = "Read and write forms"
description = ""
weight = 12
draft = true
+++

<!-- The form syntax should change https://lokad.atlassian.net/browse/LK-10421 -->

<!--TODO: insights on the form behavior https://lokad.atlassian.net/browse/LK-10422 -->

Form values represent the state of an Envision run that persists from one run to the next. Form values are intended either as a user-interaction mechanism, or a configuration mechanism. Form values are the exception to the general Envision principle to persist the entire state in tabular files.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Interactive use of form values
<!-- TODO: screenshot of the editable form missing -->
Form values are read with a `read form` statement, and they can modified through direct interaction with a dashboard with the `show form` statement.

```envision
read form with
  b : boolean
  d : date
  n : number
  t : text

show form "My form values" a1a4 with b, d, n, t
```

The resulting dashboard is editable: the form values can be modified interactively. When `Start run` button is clicked, the current form values, as displayed on the dashboard, are persisted. Those newer values becomes immediately accessible to the new run through the `read form` block.

When a new form value is introduced in a script, its value matches the default value for the datatype, e.g. 0 for `number`.

Form values are scalars. Those values can be accessed with the special prefix `form`, however, this prefix isn't a table, merely a namespace for form values.

```envision
read form with
  n : number

k = n + 1 // scalar addition

show scalar "My counter" with k
```

It is possible to use arbitrary scalar expressions in `show form`, as long as the binding with the original form value is stated explicitely through the `form:` option.

```envision
read form with
  n : number

k = n + 1 // scalar addition

show form "Click 'Start run' to increase this counter" with 
  k form:"n"
```

The above script auto-increments the counter `n` whenever a new run is started.

### Configuration use of form values

Form values are accessible at compile-time. This feature is intended to support the control of other `read` statements through form values.

```envision
read form with
  folder : text

read "/\{folder}/orders.tsv" as T max 1m with
  Quantity : number

show scalar "Total" with sum(T.Quantity)
```

Here, form values are effectively equivalent to configuration settings for the run, as there are no user-interaction involved.

Beyond the `show form` tile, there are two other mechanisms available to override form values:

* The code editor: in the right sidebar named _Options_, the form values can be edited.
* The 

### Binding form values

```envision
read form with
  t : text
  n : number
  d : date
  b : boolean

x = "1"

show form "" with
  x form:"t"
```

## Writing form values

TODO: show form
TODO: code editor control
TODO: runflow control



## Template and instances

TODO: template and instances
