+++
title = "taskUrl"
+++

## taskUrl(task: number) 🡒 text, pure function

Produces an [URL](../../stu/url/) that points to the Discuss task with identifier `task`.

```envision
show menu "Specifications" with 
  "General product rules"          { href: #(taskUrl(1000)) }
  "Electronics category overrides" { href: #(taskUrl(2000)) }
```

Cannot be called on [try.lokad.com](https://try.lokad.com/).

## taskUrl(task: number, activity: number) 🡒 text, pure function

Produces an [URL](../../stu/url/) that points to the Discuss task with identifier `task`, and scrolls down to highlight the activity with identifier `activity`.

```envision
table Items = with
  [| "A001" as Id, "B2B" as Category |]
  [| "A002"      , "B2B"             |]
  [| "B123"      , "B2C"             |]
  [| "C221"      , "Other"           |]

Items.Decision, Items.Reason = match Items.Category with
  "B2B" -> (true, taskUrl(1000, 123))
  "B2C" -> (false, taskUrl(1000, 215))
  ..    -> (false, "")

show table "Catalog" with
  Items.Id
  Items.Category
  Items.Decision { href: #[Items.Reason] }
```

Cannot be called on [try.lokad.com](https://try.lokad.com/).
