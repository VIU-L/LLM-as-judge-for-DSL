+++
title = "forex"
+++

## forex, function

```envision
def pure forex(amount: number, origin: text, destination: text, d: date): number
```

Returns the `amount` expressed in the currency `origin` into the equivalent amount in the currency `destination` according to the historical rates at the specified date `d`.

- `amount`: the number to be converted from currency `origin` to currency `destination`.
- `origin`: the currency from which to perform the conversion, as a three-letter code. 
- `destination`: the currency to which to perform the conversion, as a three-letter code.
- `d`: the historical exchange rates for this date will be used for the conversion.

### Example

```envision
table T = with
  [| as Year |]
  [| 2016 |]
  [| 2017 |]
  [| 2018 |]
  [| 2019 |]
  [| 2020 |]

show table "1 USD in EUR" a1b6 with
  T.Year
  forex(1, "USD", "EUR", date(T.Year, 1, 1)) as "Rate"
```

This outputs the following exchange rate table: 

| Year | Rate |
|---|---|
| 2016 | 0.92
| 2017 | 0.95
| 2018 | 0.83
| 2019 | 0.87
| 2020 | 0.89

### Remarks

The origin and destination currencies should be given with their canonical [three-letter codes](https://en.wikipedia.org/wiki/ISO_4217), such as `"USD"` or `"EUR"`. Lokad supports about 30 currencies leveraging the data provided by the [European Central Bank](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html) and the [Bank for International Settlements](https://www.bis.org/). To determine if a currency is supported by Lokad, call function [iscurrency](/reference/ghi/iscurrency/).

#### Discontinued currencies

Every currency has a date after which no further exchange rates are available. This is mostly used to avoid using a foreign exchange rate from the future, but in the case of a discontinued currency, this date can be far into the past. You can determine this date by calling function [lastForex](/reference/jkl/lastforex/). 

#### Missing rates

Foreign exchange rates are not published on week-ends or on bank holidays. Some currencies may have further periods of missing data, for various geopolitical or administrative reasons. For those dates, the function will instead use the last known foreign exchange rate before that point.

#### Recent rates

When requesting an exchange rate for the three days preceding the date when the script is executed, be aware that the data may not have yet been published by our sources or retrieved by our system. For this three-day period, unless the data happens to be available, the last known rate will be used instead, without warning.  

### Errors

Calling `forex` with a currency that is not supported and result in an error message (this will become a fatal error in the future): 

> Unknown currency 'XYZ'.

Calling `forex` with a date after the last available date for the currency will use the last known exchange rate, and produce a warning  message: 

> No forex data for USD on date 2024-10-13 : last known date is 2024-10-03

Calling `forex` with a date before the currency became tracked will also result in an error message (this will become a fatal error in the future). This is almost impossible, since most currencies have been tracked since before 2001-01-01 (the minimum representable date in Envision), and only a handful of currencies have not. For example, the Mauritius rupee `"MUR"`: 

> No forex data for 'MUR' on 2001-01-01.

### Recipes and Best Practices

When the raw financial data is provided in multiple currencies, it is recommended to convert that data into a single preferred currency as early as possible in the processing pipeline. 

After the initial preprocessing scripts, if any intermediate data column still contains an amount expressed in a currency stored in another data column, follow the convention of adding `Currency` to the name of the first column, keeping the two columns close together, and documenting the multiple currency aspect on the first column. For example: 

```envision
schema '/clean/sales.ion' with 
  Ref : text
  Loc : text
  OrderDate : date
  /// Total amount sold, expressed in 'AmountCurrency'
  Amount : number
  AmountCurrency : text
```

### See also

* [lastForex](/reference/jkl/lastforex/)
* [iscurrency](/reference/ghi/iscurrency/)
