+++
title = "smudge"
+++

<!-- TODO: 'smudge' is lacking a reference documentation -->

## smudge{type 'a}(T.a : 'a, T.b : boolean) 🡒 T.'a, ordered aggregator

Takes an incomplete vector of `T.a` and a Boolean vector `T.b` that determines where the valid values are present. Returns a full vector of valid values, which has been completed by spreading valid values into the non-valid ones. More precisely, the output vector is built by looking at every line, group by group (if there is a `by` argument) and following the ascending `sort`, and replacing any non-valid value by the last value that has been seen, or by a default value if no valid value has yet been seen in the group.
