+++
title = "replace"
+++

<!--The 'replace' function is too tolerant with regards of broken arguments
https://lokad.atlassian.net/browse/LK-6763 -->

## replace(source: text, pattern: text, replacement: text) 🡒 text, const pure function

Replaces in the `source` text value all the occurrence of `pattern` by the `replacement` value.

```envision
source = "Hello World!"

show summary "" a1c2 with
  replace(source, "l", "L") // returns "HeLLo WorLd!"
  replace(source, " ", "___") // returns "Hello___World!"
  replace(source, " World", "") // returns "Hello!"
```

## See also

* The [SUBSTITUTE](https://support.office.com/en-ie/article/substitute-function-6434944e-a904-4336-a9b0-1e58df3bc332) function of Excel, omitting the `instance_num` argument.
