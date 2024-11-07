+++
title = "lastForex"
+++

## forex(origin: text, destination: text) 🡒 date, pure function

Returns the date of the latest exchange rate found for a pair of currencies. The currencies should be encoded with their canonical [three-letter codes](https://en.wikipedia.org/wiki/ISO_4217). Not all exchange rates are uploaded daily to the [European Central Bank](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html).

```envision
table T = with
  [| as Code |]
  [| "JPY" |]
  [| "USD" |]
  [| "EUR" |]

show table "to CHF" a1b3 with
  T.Code
  lastForex(T.Code, "CHF")
```

## See also

* [forex](../../def/forex/)
* [iscurrency](../../ghi/iscurrency/)
