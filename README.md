# sphinx-localtime: automatic local timezone HTML conversion

This allows you to define a time with a timezone, and HTML renders
will show it converted to the apparent local timezone, with a tooltip
with the original time.

How it works:

* The role contains a date and optional format:

  ```
  :localtime:`10:00 August 8, 2024`
  :localtime:`10:00 August 8, 2024 (HH:MM)`
  ```
* At build time, `python-dateutil` parses those dates and converts it
  to UTC.
* It embeds the UTC timestamp and some javascript into the built HTML
  file.  When rendered, `dayjs` converts it to `HH:MM` or the format
  in parentheses.


## Installation

`pip install
https://github.com/coderefinery/sphinx-localtime/archive/main.zip`
(PyPI release to come later)

Add `sphinx_localtime` to extensions in conf.py


## Usage

The time format can be anything parsed by `dateutil.parser.parse`.  A
parenthesized time format (in the form in
<https://day.js.org/docs/en/display/format>) is used for the output.
The default output format is `HH:MM`.  Note the escapes aren't
`printf` standard but what is used by `dayjs`.

ReST::
```
:localtime:`13 Aug 2024 10:00:00 +03:00`
:localtime:`13 Aug 2024 10:00:00 +03:00  (D MMM HH:mm)`

:localtime2:`13 Aug 2024  (zzz)`
```

MyST:

```
{localtime}`13 Aug 2024 10:00:00 +03:00`
{localtime}`13 Aug 2024 10:00:00 +03:00  (D MMM HH:mm)`

{localtime2}`13 Aug 2024 (zzz)`
```

Rendered:
```
10:00
13 Aug 10:00

Eastern European Summer Time     # has alternative hover text without original date
```


## Specifying timezones

In order for this to work, you need to specify a timezone in your
original date in a format that `dateutil.parser.parse` can
understand.  This seems to be harder than it looks (if anyone can
help: please do!)

* Using `+03:00` and similar seems safe.
* Using long names like `Europe/Helsinki` would be good but
  `dateutil.parser.parse` doesn't recognize them.
* Short abbreviations like `EDT`, `EEST` are would work, but we need a
  generate a list of them all, but they aren't necessarily
  unique. (`pytz.all_timezones_set` is a starting point but it doesn't
  have summer times, for example).
  * It *does* work for your local timezone.  So it'll act differently
    on different build hosts...

Currently it is safest to use `+03:00`.



## Status and development

Non-HTML builders work but don't give the most useful output (someone
good at Docutils/Sphinx doctrees could help here).  The javascript
could be embedded so that it's not an external resource.  Timezone
abbreviation lookup could be improved.  The name could be
still changed.

Beta, contributions welcome.
