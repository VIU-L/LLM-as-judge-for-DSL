+++
title = "syncUrl"
+++

## syncUrl(id: number) 🡒 text, pure function

Produces an [URL](../../stu/url/) that points to the data synchronization script with identifier `id`.

```envision
show menu "Third party inputs" with 
  "Contoso"  { href: #(syncUrl(1000)) }
  "Fabrikam" { href: #(syncUrl(2000)) }
```

End users will usually not be granted access to see synchronization scripts, so this function is mostly intended to design tools for internal use.

This function cannot be called on [try.lokad.com](https://try.lokad.com/).
