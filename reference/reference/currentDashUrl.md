+++
title = "currentDashUrl"
+++

## currentDashUrl() -> text, pure function

Produces an [URL](../../stu/url/) which, when visited, redirects to the dashboard of the run in which it was executed.

```envision
schema '/logs.ion' with 
  Operation : text
  Url : text

read '/logs.ion' as Logs 

// Append the current operation to the logs
table Logs max 1m = with 
  [| Logs.Operation as Operation, Logs.Url as Url  |]
  [| "Pre-processing",            currentDashUrl() |] 

write Logs as '/logs.ion' 
```

Cannot be called from [modules](/language/modules/) or from [user-defined functions](/language/functions/), or on [try.lokad.com](https://try.lokad.com/).

The main use case for this function is to write its output to a file that is then loaded from another script so that it can produce a link to this specific run.

## See also

- [sliceUrl](../../stu/sliceurl/) for the URL to point to a specific slice on the dashboard of this run. 
- [dashUrl](../../def/dashurl/) for the URL to point to the latest dashboard produced by a script, instead of the one produced by the current run.
- [sliceSearchUrl](../../stu/slicesearchurl/) for the URL to point to a slice, by name, on the latest dashboard produced by a script.
