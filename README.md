# sphinx-localtimezone: automatic local timezone HTML conversion

This allows you to define a time with a timezone, and HTML renders
will show it converted to the apparent local timezone, with a tooltip
with the original time.

## Installation

pip, add `sphinx_localtimezone` to extensions in conf.py

## Usage

The time format can be anything parsed by `dateutil.parser.parse`.  A
parenthesized time format (in the form in
<https://day.js.org/docs/en/display/format>) is used for the output

ReST::
```
:local-timezone:`13 Aug 2024 10:00:00 EEST`
:local-timezone:`13 Aug 2024 10:00:00 EEST  (D MMM HH:mm)`
```

MyST:

```
{local-timezone}`13 Aug 2024 10:00:00 EEST`
{local-timezone}`13 Aug 2024 10:00:00 EEST  (D MMM HH:mm)`
```

Rendered:
```
10:00
13 Aug 10:00
```


# Status and development

Non-HTML may not work.

Beta and contributions welcome.
