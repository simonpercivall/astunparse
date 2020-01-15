Changelog
=========

Here's the recent changes to AST Unparser.

1.6.3 - 2019-12-22
~~~~~~~~~~~~~~~~~~

* Add full support for Python 3.8

1.6.2 - 2019-01-19
~~~~~~~~~~~~~~~~~~

* Add support for the Constant node in Python 3.8
* Add tests to the sdist

1.6.1 - 2018-10-03
~~~~~~~~~~~~~~~~~~

* Fix the roundtripping of very complex f-strings.

1.6.0 - 2018-09-30
~~~~~~~~~~~~~~~~~~

* Python 3.7 compatibility

1.5.0 - 2017-02-05
~~~~~~~~~~~~~~~~~~

* Python 3.6 compatibility
* bugfix: correct argparser option type

1.4.0 - 2016-06-24
~~~~~~~~~~~~~~~~~~

* Support for the ``async`` keyword
* Support for unparsing "Interactive" and "Expression" nodes

1.3.0 - 2016-01-17
~~~~~~~~~~~~~~~~~~

* Python 3.5 compatibility

1.2.0 - 2014-04-03
~~~~~~~~~~~~~~~~~~

* Python 2.6 through 3.4 compatibility
* A new function ``dump`` is added to return a pretty-printed version
  of the AST. It's also available when running ``python -m astunparse``
  as the ``--dump`` argument.

1.1.0 - 2014-04-01
~~~~~~~~~~~~~~~~~~

* ``unparse`` will return the source code for an AST. It is pretty
  feature-complete, and round-trips the stdlib, and is compatible with
  Python 2.7 and Python 3.4.

  Running ``python -m astunparse`` will print the round-tripped source
  for any python files given as argument.
