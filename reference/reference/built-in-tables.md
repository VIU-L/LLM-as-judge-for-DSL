+++
title = "Built-in Tables"
+++

## Built-in tables

The following tables are always defined in every script: 

 - [Scalar](/reference/stu/scalar): has exactly one line, cannot be filtered. Any variable or literal without an explicit table prefix belongs in this table.
 - [Files](/reference/def/files): has one line for each file that was captured by `read` statements in the script.

The following tables can be defined in scripts that use certain features:

 - [Day](/reference/def/day): automatically defined when the `date` dimension is used.
 - [Week](/reference/vwx/week): automatically defined alongside table `Day`.
 - [Month](/reference/mno/month): automatically defined alongside table `Day`.
 - [Slices](/reference/stu/slices): automatically defined when the script becomes sliced, and contains one line per slice. 

