.. Test documentation master file, created by
   sphinx-quickstart on Tue Aug 13 23:27:54 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tests of sphinx-localtimezone
=============================

Tests of sphinx-localtimezone:

localtime
---------

The `localtime` role:

* ``13 Aug 2024 10:00:00 +03:00``: :localtime:`13 Aug 2024 10:00:00 +03:00`
* ``13 Aug 2024 10:00:00 EEST``: :localtime:`13 Aug 2024 10:00:00 EEST`
* ``13 Aug 2024 10:00:00 EEST (D MMM HH:mm)``: :localtime:`13 Aug
  2024 10:00:00 EEST  (D MMM HH:mm)`
* ``13 Aug 2024 10:00:00 EEST (HH:mm z)``: :localtime:`13 Aug
  2024 10:00:00 EEST  (HH:mm z)`
* ``13 Aug 2024 10:00:00 EEST (HH:mm zzz)``: :localtime:`13 Aug
  2024 10:00:00 EEST  (HH:mm zzz)`

localtime2
----------

The `localtime2` role has a different hover text and is designed for
showing the timezone without a date.

* ``13 Aug 2024 (zzz)``: Your detected timezone
  is :localtime2:`13 Aug 2024 (zzz)`
* ``13 Aug 2024 (z)``: Your detected timezone
  is :localtime2:`13 Aug 2024 (z)`

Test of invalid format
----------------------

* :localtime:`This is an invalid time`


Repeat of one of the above
--------------------------
(for use in testing caching in non-HTML formats)

* ``13 Aug 2024 10:00:00 +03:00``: :localtime:`13 Aug 2024 10:00:00 +03:00`


Other pages
-----------

.. toctree::

   empty
