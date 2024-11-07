+++
title = "sanitize"
+++
<!--- git commit -m "LK-13652 <message>" --->
## sanitize(source: text) 🡒 text, pure

There are cases where the text that the user sees is different from the text that user expects when working with it or processing it: The text might contain so-called invisible characters that can appear like regular space characters on the screen or they do not appear at all, hence truly becoming invisible. Such invisible characters can for example be tabulators, no-break spaces or Hangul Fillers. A list of invisible characters that are supported by the `sanitize` function will be provided in the next section. For further study, an exhaustive list of invisible Unicode characters can be found on https://invisible-characters.com.

Envision's [escape](../../def/escape/) function is very useful in making such characters visible by replacing the character itself with its Unicode notation, but it can become cumbersome to clean up the text and remove or [replace](../../pqr/replace/) those characters for safer processing because that can require several [replace](../../pqr/replace/) operations for each of the invisible characters contained in the source text.

The `sanitize` function removes all supported invisible characters from the source argument and returns a cleaned-up version of the source text.

### Example

This example illustrates using the function with accepted characters:

```envision
t = "Sanitizing a no-break-space\u00A0, a Hangul Filler\u3164, and a tab\t."

l=strlen(t)
show scalar "The untouched text source. \{l} Characters." a1e1 with t

show scalar "Revealing the invisible characters. \{l} Characters." a2e2 with escape(t)

t = sanitize(t)
l = strlen(t)

{ textBold: true }
show scalar "The sanitized text. \{l} Characters." a4e4 with t
```

## Supported Invisible Characters

The `sanitize` function will scan for and remove invisible characters from the following list:

| Unicode | Unicode Character Name |
|---|---|
| `U+0009` | CHARACTER TABULATION |
| `U+00A0` | NO-BREAK SPACE |
| `U+00AD` | SOFT HYPHEN |
| `U+034F` | COMBINING GRAPHEME JOINER |
| `U+061C` | ARABIC LETTER MARK |
| `U+115F` | HANGUL CHOSEONG FILLER |
| `U+1160` | HANGUL JUNGSEONG FILLER |
| `U+17B4` | KHMER VOWEL INHERENT AQ |
| `U+17B5` | KHMER VOWEL INHERENT AA |
| `U+180E` | MONGOLIAN VOWEL SEPARATOR |
| `U+2000` | EN QUAD |
| `U+2001` | EM QUAD |
| `U+2002` | EN SPACE |
| `U+2003` | EM SPACE |
| `U+2004` | THREE-PER-EM SPACE |
| `U+2005` | FOUR-PER-EM SPACE |
| `U+2006` | SIX-PER-EM SPACE |
| `U+2007` | FIGURE SPACE |
| `U+2008` | PUNCTUATION SPACE |
| `U+2009` | THIN SPACE |
| `U+200A` | HAIR SPACE |
| `U+200B` | ZERO WIDTH SPACE |
| `U+200C` | ZERO WIDTH NON-JOINER |
| `U+200D` | ZERO WIDTH JOINER |
| `U+200E` | LEFT-TO-RIGHT MARK |
| `U+200F` | RIGHT-TO-LEFT MARK |
| `U+202F` | NARROW NO-BREAK SPACE |
| `U+205F` | MEDIUM MATHEMATICAL SPACE |
| `U+2060` | WORD JOINER |
| `U+2061` | FUNCTION APPLICATION |
| `U+2062` | INVISIBLE TIMES |
| `U+2063` | INVISIBLE SEPARATOR |
| `U+2064` | INVISIBLE PLUS |
| `U+206A` | INHIBIT SYMMETRIC SWAPPING |
| `U+206B` | ACTIVATE SYMMETRIC SWAPPING |
| `U+206C` | INHIBIT ARABIC FORM SHAPING |
| `U+206D` | ACTIVATE ARABIC FORM SHAPING |
| `U+206F` | NOMINAL DIGIT SHAPES |
| `U+2800` | BRAILLE PATTERN BLANK |
| `U+3000` | IDEOGRAPHIC SPACE |
| `U+3164` | HANGUL FILLER |
| `U+FEFF` | ZERO WIDTH NO-BREAK SPACE |
| `U+FFA0` | HALFWIDTH HANGUL FILLER |

### Valid source text

The function only accepts text containing characters from the following Unicode blocks:

| Character Range | Unicode Block |
|---|---|
| `U+0020 – U+007F` | Basic Latin (without C0 control codes) |
| `U+0080 - U+009F` | C1 control codes |
| `U+00A0 – U+00FF` | Latin-1 Supplement |
| `U+0100 – U+017F` | Latin Extended-A |
| `U+0180 – U+024F` | Latin Extended-B |
| `U+0250 – U+02AF` | IPA Extensions |
| `U+02B0 – U+02FF` | Spacing Modifier Letters |
| `U+0300 - U+036F` | Combining Diacritical Marks |
| `U+0370 - U+03FF` | Greek/Coptic |
| `U+0400 - U+04FF` | Cyrillic |
| `U+2010 - U+2027` | General Punctuation |
| `U+2030 - U+205E` | General Punctuation |
| `U+2061 - U+2064` | General Punctuation |
| `U+20A0 - U+20C0` | Currency Symbols |

### Invalid source text

The `sanitize` function restricts the text that it processes to supported languages and symbols that can be expected in supply chain forms.

Characters from the following Unicode ranges are not accepted by the function:

| Unicode Range | Unaccepted Unicode Block |
|---|---|
| `U+0000 - U+001F` | C0 Control Codes |
| `U+0500 - U+1FFF` | Unsupported Languages |
| `U+2070 – U+209F` | Superscripts and Subscripts |
| `U+20D0 and above` | Unsupported Languages, Emojis, Dingbats and Symbols |

If any such characters are contained in the source argument, Envision will respond with a message using this format:

`
sanitize(): "<source>" has invalid character \u<character value> '<Unicode character>'.
`

For example, when trying

```envision
t = sanitize("Text with Dingbats ✂")
```

Envision will report the following:

`
sanitize(): "Text with Dingbats ✂" has invalid character \u2702 '✂'.
`

Passing a source text with emojis will produce a similar respone:

```envision
t = sanitize("Text with emoji 🙂")
```

Envision will then report:

`
sanitize(): "Text with emoji 🙂" has invalid character \uD83D\uDE42 '🙂'.
`

## See also

- [escape](../../def/escape/)
- [replace](../../pqr/replace/)
