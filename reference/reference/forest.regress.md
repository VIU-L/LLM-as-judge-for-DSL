+++
title = "forest.regress"
+++

## forest.regress(..) 🡒 ranvar, function

The function `forest.regress` is a function with labeled arguments. It gives access to a random forest regression algorithm. The function expects two tables to be used. First a _training_ table, and second an _evaluation_ table. The function learns the random forest on the training table, and then evaluates the model against the evaluation table.

Here is an illustrating script:

```envision
// Training dataset with known labels
table Example = with
  [| as Id, as A, as B,  as C,     as Label |]
  [| 1,     5,    true,  "high",   42       |]
  [| 2,     3,    false, "low",    35       |]
  [| 3,     4,    true,  "medium", 38       |]
  [| 4,     2,    false, "high",   30       |]
  [| 5,     6,    true,  "low",    45       |]

// Evaluation dataset without labels
table Sample = with
  [| as Id, as A, as B,  as C     |]
  [| 11,    6,    true,  "medium" |]
  [| 12,    2,    false, "high"   |]

// Perform random forest regression
// Beware arguments are labeled
// 'Sample.Label' is a 'ranvar'
Sample.Label = forest.regress( // arguments are newline delimited
  training: Example.A, Example.B, Example.C
  label: Example.Label
  evaluation: Sample.A, Sample.B, Sample.C) // here is the closing comma

// Display the predicted labels
show table "Predicted Labels" with Sample.Id, Sample.Label
```

For every line of the evaluation table (the `Sample` table in the script above), the function returns a `ranvar` which represent the distribution of predictions by the forest.

The function wraps into a single call what is usually a 2-stage process of _learning_ followed by _inference_. This design is intentional and removes the need to introduce a special datatype for the random forest model within Envision.

The function performs a probabilistic forecast over integers taking advantage of the `ranvar` datatype of Envision. This design is motivated by the fact that the vast majority of data being regressed in supply chain are discrete. This design diverges from the more usual random forest settings where the forest predictions are averaged out directly.

The function `forest.regress` supports

* features of types `number`, `text`, `bool`. The `number` features are treated as numerical. If a categorical feature is intended, then convert the `number` to `text` with the `text(Example.A)` function.
* Up to 16 distinct features are supported, with at most 8 features of the `number` type (numerical variables), and at most 8 features of the `boolean` or `text` types (categorical variables).

Optionally, a text vector of words can be provided as `trainingBow` and `evaluationBow`: here the text value is treated as a bag-of-words, and analysed in terms of words occurrences.

### forest.regress, with bag-of-words

In addition to its numerical and categorical features, the function `forest.regress` also supports a single feature to be treated as a space-delimited bag-of-word.

Here is an illustrating script:

```envision
// Training dataset with known labels
table Example = with
  [| as Id, as A, as B,  as C,    as D,               as Label |]
  [| 1,     5,    true,  "high",  "sun rain",         42       |]
  [| 2,     3,    false, "low",   "cloud snow",       35       |]
  [| 3,     4,    true,  "medium","wind storm",       38       |]
  [| 4,     2,    false, "high",  "fog mist",         30       |]
  [| 5,     6,    true,  "low",   "hail thunder ice", 45       |]

// Evaluation dataset without labels
table Sample = with
  [| as Id, as A, as B,  as C,    as D        |]
  [| 3,     6,    true,  "medium","sun storm" |]
  [| 4,     2,    false, "high",  "cloud fog" |]

// Perform random forest regression
// Beware arguments are labeled
// 'Sample.Label' is a 'ranvar'
Sample.Label = forest.regress( // arguments are newline delimited
  training: Example.A, Example.B, Example.C
  trainingBow: Example.D // space-separated
  label: Example.Label
  evaluation: Sample.A, Sample.B, Sample.C
  evaluationBow: Sample.D) // here is the closing comma

// Display the predicted labels
show table "Predicted Labels" with Sample.Id, Sample.Label
```
