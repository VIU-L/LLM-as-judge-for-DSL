+++
title = "markdown"
+++

## markdown, datatype

The `markdown` datatype is intended to for [Markdown](http://commonmark.org/help/) text pieces. Literals can be introduced with the triple-quote syntax.

```envision
m = """Hello **World**"""
show markdown "" a1b2 with m
```

Markdown literals support multi-line entries.

```envision
m = """
Hello

World
"""

show markdown "" a1b2 with m
```

The `markdown` datatype is restricted to the `Scalar` table. Unlike the `text` datatype, the `markdown` datatype does not have a limit at 256 characters.

Interpolation is also supported for the `markdown` datatype:

```envision
a = "Hello" // text type
b = """World""" // markdown type

// Compose a markdown value through interpolation
show markdown "" a1b2 with """\{a}, \{b}!""" // 'Hello, World!'
```

## markdown, tile type

The `markdown` tile is intended to `markdown` values.

```envision
show markdown "" a6h6 with """
# Part A
## Subpart A.1
A list of **important** remarks.

* remark 1
* remark 2
* remark 3

## Subpart A.2
# Part B

Less important remarks.
"""
```

We recommend leaving the title empty, as the tile title is usually redundant with the title defined within the Markdown section itself, as illustrated by:

```envision
show markdown "" with """ ... """
```

The markdown tile offers a printable version. In order to access this feature, expand the markdown tile with single click on the tile itself, and then click the button `Display plain tile` in the top right corner.
