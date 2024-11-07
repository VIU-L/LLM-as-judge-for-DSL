+++
title = "extend.split"
+++

## extend.split(A.Source : text, S.Separator : text) 🡒 B.*, table function

Generates all the tokens obtained by splitting the source text values according to specificed separators. Empty tokens are omitted. The first argument must be the source text values. The second argument must be the separators. The returned table contains two vectors `Token : text` and `Position : number`.

```envision
table Phrases = with
  [| as X                |]
  [| "|blue berry|fruit" |]
  [| "fast|||red||fox"   |]
  [| "big  t i ger "     |]

table Separators = with
  [| as S |]
  [| " "  |]
  [| "|"  |]

table T = extend.split(Phrases.X, Separators.S)
T.Check = substr(Phrases.X, T.Position, strlen(T.Token))

show table "Tokens" a1c10 with
  Phrases.X
  T.Token
  T.Position
  substr(Phrases.X, T.Position, strlen(T.Token)) // matches 'T.Token'
```

The table function fails if:

* The separator table is empty.
* The separator table contains more than 100 lines.
* A separator is empty.

**Signature** :

```envision-proto
/// Create a list of tokens splitting input text values.
/// Empty tokens are omitted. Max 100 separators.
tablefunc extend.split<Phrases,Separators>(
    /// Input text value to be split.
    Phrases.Source : text,
    /// Table must not be empty. Separator must not be empty text.
    Separators.Separator : text
) : {
    /// The non-empty token.
    Token : text,
    /// The index of the first char in the original text value.
    Position : number
}
```

## extend.split(A.Source : text, S.Separator : text, U.Unit : text) 🡒 B.*, table function

Generates all the tokens obtained by splitting the source text values according to specificed separators and according to the specified units. Empty tokens are omitted.

* The first argument must be the source text values.
* The second argument must be the separators.
* The third argument must be the units.

Source values are first split according to the delimiters. If a token ends with a unit, and if the prefix (before the unit) starts and ends with a digit, then the token is split in two.

The returned table contains two vectors `Token : text` and `Position : number`.

```envision
table Phrases = with
  [| as X                |]
  [| "|blue berry|12kg"  |]
  [| "fast|||101cm||fox" |]
  [| "big  t i ger "     |]

table Separators = with
  [| as S |]
  [| " "  |]
  [| "|"  |]

table Units = with
  [| as U |]
  [| "kg" |]
  [| "cm" |]

table T = extend.split(Phrases.X, Separators.S, Units.U)
T.Check = substr(Phrases.X, T.Position, strlen(T.Token))

show table "Tokens" a1c10 with
  Phrases.X
  T.Token
  T.Position
  substr(Phrases.X, T.Position, strlen(T.Token)) // matches 'T.Token'
```

The table function fails if:

* The separator table is empty.
* The separator table contains more than 100 lines.
* The unit table contains more than 100 lines.
* A separator is empty.
* A unit is empty.

**Signature** :

```envision-proto
/// Create a list of tokens splitting input text values.
/// A unit-split occurs if a token ends with the unit
/// and if the unit is immediately preceded by a digit.
/// Empty tokens are omitted. Max 100 separators.
/// Max 100 units.
tablefunc extend.split<Phrases,Separators,Units>(
    /// Input text value to be split.
    Phrases.Source : text,
    /// Separator must not be empty text.
    Separators.Separator : text,
    /// Table must not be empty. Unit must not be empty text.
    Units.Unit : text
) : {
    /// The non-empty token.
    Token : text,
    /// The index of the first char in the original text value.
    Position : number
}
```
