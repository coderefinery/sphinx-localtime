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
:localtime:`13 Aug 2024 10:00:00 EEST`
:localtime:`13 Aug 2024 10:00:00 EEST  (D MMM HH:mm)`
```

MyST:

```
{localtime}`13 Aug 2024 10:00:00 EEST`
{localtime}`13 Aug 2024 10:00:00 EEST  (D MMM HH:mm)`
```

Rendered:
```
10:00
13 Aug 10:00
```


# Status and development

Non-HTML builders work but don't give the most useful output.  The
javascript could be embedded so that it's not an external resource.
The name could be still changed.

Beta and contributions welcome.
