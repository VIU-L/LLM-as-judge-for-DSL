+++
title = "Envision Reference"
url = "reference"
weight = 5
alwaysopen = false
+++

This section catalogues the features and capabilities of both the Envision language and its standard library. This section is intended for an advance audience who has already mastered the Envision basics.

**Table of contents**
{{< toc >}}{{< /toc >}}

## Keywords

The list of words that have built-in semantic in Envision.

**Reserved keywords:** [and](abc/and/) [as](abc/as/) [at](abc/at/) [auto](abc/auto/) [autodiff](abc/autodiff/) [by](abc/by/) [const](abc/const/) [cross](abc/cross/) [def](def/def/) [default](def/default/) [delete](def/delete/) [desc](def/desc/) [each](def/each/) [else](ghi/if/) [enum](def/enum/) [expect](def/expect/) [export](def/export/) [fail](def/fail/) [false](def/false/) [for](def/for/) [group](ghi/group/) [if](ghi/if/) [import](ghi/import/) [in](ghi/in/) [into](ghi/into/) [keep](jkl/keep/) [loop](jkl/loop/) [match](mno/match/) [mod](mno/mod/) [montecarlo](mno/montecarlo) [not](mno/not/) [or](mno/or/) [order](mno/order/) [over](mno/over/) [params](pqr/params/) [process](pqr/process/) [read](pqr/read/) [return](pqr/return/) [sample](stu/sample/) [scan](stu/scan/) [show](stu/show/) [sort](stu/sort/) [span](stu/span/) [table](stu/table/) [then](ghi/if/) [true](stu/true/) unsafe [when](vwx/when/) [where](vwx/where/) [with](vwx/with/) [write](vwx/write/)

**Contextual keywords:**  [assert](abc/assert/) [barchart](abc/barchart/) [boolean](abc/boolean/) [chart](abc/chart/) [date](def/date/) [flagset](def/flagset/) [form](def/form/) [histogram](ghi/histogram/) interval [label](jkl/label/) latest [linechart](jkl/linechart/) logo [max](mno/max/) [min](mno/min/) [markdown](mno/markdown/) [month](mno/month/) [nosort](mno/nosort/) [number](mno/number/) [partitioned](pqr/partitioned/) [piechart](pqr/piechart/) [plot](pqr/plot/) private [pure](pqr/pure/) [ranvar](pqr/ranvar/) [scatter](stu/scatter/) [scalar](stu/scalar/) [single](stu/single/) [slicepicker](stu/slicepicker/) [slicetree](stu/slicetree/) [small](stu/small/) [summary](stu/summary/) [tabs](stu/tabs/) [text](stu/text/) [upload](stu/upload/) [week](vwx/week/) [whichever](vwx/whichever/) [zedfunc](yz/zedfunc/)

**Keywords reservd for later:** define draw foreach index until while

## Operators

The operators below are listed in increasing order of precedence. For instance, since `and` is before `or`, then `A or B and C` is interpreted as `A or (B and C)`. Operators with the same precedence are grouped left-to-right: `A * B / C` is `(A * B) / C`.

* [`..`](_/dots2/)
* [if then else](ghi/if/)
* (unary) [`+`](_/add/)  [`-`](_/minus/) [`~`](_/tilde/) [`not`](mno/not/)
* [`^`](_/power/)
* (binary) [`*`](_/multiply/) [`/`](_/divide/) [`/.`](_/divide/) [`mod`](mno/mod/)
* [`+`](_/add/) [`-`](_/minus/)
* ([comparisons](_/compare/)) `<` `>` `<=` `>=` `==` `!=` [`~~`](_/tilde2/) [`!~`](_/tilde2/) [in](ghi/in/)
* [`and`](abc/and/)
* [`or`](mno/or/)
* [`into`](ghi/into/)
* [`...`](_/dots3/)
* [`[]`](_/lookup/)
* [`.`](_/dot/)

## Aggregators

The aggregators are similar to functions, but they benefit from a richer syntax with options. Below, we list the aggregators supported by Envision.

**Basic:** [argmax](abc/argmax/) [argmin](abc/argmin/) [argwhichever](abc/argwhichever/) [areSame](abc/aresame/) [count](abc/count/) [distinct](def/distinct/) [distinctapprox](def/distinctapprox/) [max](mno/max/) [min](mno/min/) [product](pqr/product/)  [single](stu/single/) [sum](stu/sum/)

**Logic:** [all](abc/all/) [any](abc/any/) [same](stu/same/) [whichever](vwx/whichever/)

**Ordered:** [changed](abc/changed/) [concat](abc/concat/) [first](def/first/) [join](jkl/join/) [last](jkl/last/) [smudge](stu/smudge/)

**Statistics:** [avg](abc/avg/) [entropy](def/entropy/) [median](mno/median/) [mode](mno/mode/) [percentile](pqr/percentile/) [stdev](stu/stdev/) [stdevp](stu/stdevp/)

**Ranvar:** [mixture](mno/mixture/) [ranvar](pqr/ranvar/) [ranvar.buckets](pqr/ranvar.buckets/) [sum](stu/sum/)

**Zedfunc:** [sum](stu/sum/)

## Functions

The primary purpose of functions is to extend the capabilities of Envision whenever the basic language syntax would not be sufficient. Below, we list the functions supported by Envision.

**Mathematics:** [abs](abc/abs/) [arground](abc/arground/) [ceiling](abc/ceiling/) [cos](abc/cos/) [exp](def/exp/) [expsmooth](def/expsmooth/) [floor](def/floor/) [log](jkl/log/) [logGamma](jkl/loggamma/) [loglikelihood.logLogistic](jkl/loglikelihood.loglogistic/) [loglikelihood.normal](jkl/loglikelihood.normal/) [loglikelihood.negativeBinomial](jkl/loglikelihood.negativebinomial/) [loglikelihood.poisson](jkl/loglikelihood.poisson/) [max](mno/max/) [min](mno/min/) [noGrad](mno/nograd/) [percent](pqr/percent/) [random.binomial](pqr/random.binomial/) [random.integer](pqr/random.integer/) [random.logLogistic](pqr/random.loglogistic/) [random.negativeBinomial](pqr/random.negativebinomial/) [random.normal](pqr/random.normal/) [random.poisson](pqr/random.poisson/) [random.shuffle](pqr/random.shuffle/) [random.uniform](pqr/random.uniform/) [ratio](pqr/ratio/) [regularizationTerm](pqr/regularizationterm/) [round](pqr/round/) [roundNext](pqr/roundnext/) [sin](stu/sin/) [sqrt](stu/sqrt/) [tanh](stu/tanh/)

**Text:** [concat](abc/concat/) [contains](abc/contains/) [containsAny](abc/containsany/) [containsCount](abc/containscount/) [endsWith](def/endswith/) [escape](def/escape/) [field](def/field/) [fieldCount](def/fieldcount/) [fieldr](def/fieldr/) [indexOf](ghi/indexof/) [lowercase](jkl/lowercase/) [padLeft](pqr/padleft/) [parseDate](pqr/parsedate/) [parseNumber](pqr/parsenumber/) [parseTime](pqr/parsetime/) [printTime](pqr/printtime/) [replace](pqr/replace/) [startsWith](stu/startswith/) [strlen](stu/strlen/) [substr](stu/substr/) [text](stu/text/) [trim](stu/trim/) [tryParseDate](stu/tryparsedate/) [tryParseNumber](stu/tryparsenumber/) [tryParseTime](stu/tryparsetime/) [tryParseWeek](stu/tryparseweek/) [uppercase](stu/uppercase/)

**Calendar:** [yearChinese](yz/yearchinese/) [yearEndChinese](yz/yearendchinese/) [yearStartChinese](yz/yearstartchinese/) [date](def/date/) [dayNum](def/daynum/) [format](def/format/) [yearISO](ghi/yeariso/) [monday](mno/monday/) [month](mno/month/) [monthEnd](mno/monthend/) [monthNum](mno/monthnum/) [monthStart](mno/monthstart/) [today](stu/today/) [week](vwx/week/) [weekNum](vwx/weeknum/) [year](yz/year/) [yearEnd](yz/yearend/) [yearStart](yz/yearstart/)

**Ranking:** [argfirst](abc/argfirst/) [arglast](abc/arglast/) [assoc.quantity](abc/assoc.quantity/) [cumsub](abc/cumsub/) [cumsubfallback](abc/cumsubfallback/) [cumsum](abc/cumsum/) [fifo](def/fifo/) [priopack](pqr/priopack/) [rank](pqr/rank/) [rankd](pqr/rankd/) [smudge](stu/smudge/)

**Graph:** [canonical](abc/canonical/) [connected](abc/connected/) [hasCycles](ghi/hascycles/) [noncanonical](mno/noncanonical/) [partition](pqr/partition)

**Ranvar:** [actionrwd.demand](abc/actionrwd.demand/) [actionrwd.segment](abc/actionrwd.segment/) [cdf](abc/cdf/) [crps](abc/crps/) [dirac](def/dirac/) [dispersion](def/dispersion/) [exponential](def/exponential/) [fillrate](def/fillrate/) [forest.regress](def/forest.regress/) [int](ghi/int/) [logLogistic](jkl/loglogistic/) [mean](mno/mean/) [mixture](mno/mixture/) [negativeBinomial](mno/negativebinomial/) [normal](mno/normal/) [poisson](pqr/poisson/) [quantile](pqr/quantile/) [random.ranvar](pqr/random.ranvar/) [ranvar](pqr/ranvar/) [ranvar.periodicr](pqr/ranvar.periodicr/) [ranvar.segment](pqr/ranvar.segment/) [ranvar.uniform](pqr/ranvar.uniform/) [smooth](stu/smooth/) [spark](stu/spark/) [transform](stu/transform/) [truncate](stu/truncate/) [variance](vwx/variance/)

**UX**: [Slices](stu/slices/) [sliceSearchUrl](stu/slicesearchurl/)

**Zedfunc:** [actionrwd.reward](abc/actionrwd.reward/) [constant](abc/constant/) [diracz](def/diracz/) [int](ghi/int/) [linear](jkl/linear/) [pricebrk.f](pqr/pricebrk.f/) [pricebrk.m](pqr/pricebrk.m/) [stockrwd.c](stu/stockrwd.c/) [stockrwd.m](stu/stockrwd.m/) [stockrwd.s](stu/stockrwd.s/) [uniform](stu/uniform/) [uniform.left](stu/uniform.left/) [uniform.right](stu/uniform.right/) [valueAt](vwx/valueat/) [zoz](yz/zoz/)

**Table:** [by](abc/by/) [extend.billOfMaterials](def/extend.billofmaterials/) [extend.pairs](def/extend.pairs/) [extend.pairset](def/extend.pairset/) [extend.range](def/extend.range/) [extend.ranvar](def/extend.ranvar/) [extend.split](def/extend.split/) [single by](stu/single/) [whichever by](vwx/whichever/)

**Sets:** [flag](def/flag/) [emptySet](def/emptyset/) [union](stu/union/) [intersection](ghi/intersection/) [complement](abc/complement/) [isSubsetOf](ghi/issubsetof/) [contains](abc/contains/) [popCount](pqr/popcount/).

**Special:** [assertfail](abc/assertfail/) [Files](def/files/) [forex](def/forex/) [lastForex](jkl/lastforex/) [hash](ghi/hash/) [iscurrency](ghi/iscurrency/) [mkuid](mno/mkuid/) [nameof](mno/nameof/)  [rgb](pqr/rgb/) [solve.moq](stu/solve.moq/)

## Tiles

The tiles represent the building blocks of Envision's dashboards. Below, we list all the tiles supported by Envision.

[assert](abc/assert/) [barchart](abc/barchart/) [chart](abc/chart/) [form](def/form/) [histogram](ghi/histogram/) [label](jkl/label/) [linechart](jkl/linechart/) [markdown](mno/markdown/) [piechart](pqr/piechart/) [plot](pqr/plot/) [scalar](stu/scalar/) [scatter](stu/scatter/) [slicepicker](stu/slicepicker/) [slicetree](stu/slicetree/) [summary](stu/summary/) [table](stu/table/) [tabs](stu/tabs/) [treemap](stu/treemap/) [upload](stu/upload/)

## Special tables

The special tables do not behave exactly like the other tables:

[Day](def/day/) [Files](def/files/) [Month](mno/month/) [Scalar](stu/scalar/) [Week](vwx/week/)

<!-- phased out 
* `norminv(x: number)`: applied to a probability, returns the inverse of the normal cumulative distribution function, with mean at $0$ and a standard deviation of $1$. Similar to the [NORM.S.INV](https://support.office.com/en-us/article/norm-s-inv-function-d6d556b4-ab7f-49cd-b526-5a20918452b1) function in Excel.
* `zscore(T.X: number, T.G: any) -> number`: similar to the [STANDARDIZE](https://support.office.com/en-us/article/STANDARDIZE-function-81D66554-2D54-40EC-BA83-6437108EE775) function in Excel. The z-score of a value indicates how many standard deviations from the mean your score is within the group implicitely defined by `T.G`. If the standard deviation is equal to zero, so is the z-score.
-->
