+++
title = "URL"
+++

## URL, concepts

Envision allows representing [Uniform Resource Locators (URLs)](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Web_mechanics/What_is_a_URL) as values of the [text](/reference/stu/text/) type.

To create clickable link to a given URL, use the [`href`](/specifications/stylecode/properties/href/) StyleCode property:

```envision
TheURL = "https://en.wikipedia.org/wiki/Stockout"
show label "Learn more about Stockouts" { href: #(TheURL) } 
```

While it is safe to hard-code URLs to external websites directly in an Envision script, it is not recommended to hard-code URLs to pages in the Lokad application (such as the URLs of dashboards, scripts, files or images), as those are subject to change. Instead, please call one of the following functions to produce the correct URL on the fly:

| Function | Purpose |
|---|---|
| [`currentDashUrl()`](/reference/abc/currentdashurl/) | Open the dashboard that was produced by the executing run.
| [`dashUrl()`](/reference/def/dashurl/) | Open the latest dashboard of a script. |
| [`downloadUrl()`](/reference/def/downloadurl/) | Download a file stored in the Lokad application.
| [`fileUrl()`](/reference/def/fileurl/) | Open the folder containing a file in the Lokad file explorer.
| [`folderUrl()`](/reference/def/folderurl/) | Open a folder in the Lokad file explorer.
| [`previewUrl()`](/reference/pqr/previewurl/) | Open a preview page for a file.
| [`sequenceUrl()`](/reference/stu/sequenceurl/) | Open the page of a script sequence.
| [`sliceSearchUrl()`](/reference/stu/slicesearchurl/) | Open a specific slice of a dashboard, if it exists. |
| [`sliceUrl()`](/reference/stu/sliceurl/) | Open a specific slice of the dashboard produced by the executing run.  |
| [`syncUrl()`](/reference/stu/syncurl/) | Open the page of a sync script.
| [`taskUrl()`](/reference/stu/taskurl/) | Open a Discuss task.

Note that all of the above functions produce URLs that start with `~/`. This is automatically replaced with the correct prefix (of the form `https://go.lokad.com/<ACCOUNT>/`) when displayed with `href`. These URLs cannot be used to create cross-account links.
