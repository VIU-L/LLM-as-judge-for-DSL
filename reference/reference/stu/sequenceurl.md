+++
title = "sequenceUrl"
+++

## sequenceUrl(id: number) 🡒 text, pure function

Produces an [URL](../../stu/url/) that points to the script sequence with identifier `id`.

```envision
show menu "Sequences" with 
  "Morning" { href: #(sequenceUrl(1000)) }
  "Evening" { href: #(sequenceUrl(2000)) }
  "Weekly"  { href: #(sequenceUrl(1234)) }
```

End users will usually not be granted access to see script sequences, so this function is mostly intended to design tools for internal use.

This function cannot be called on [try.lokad.com](https://try.lokad.com/).
