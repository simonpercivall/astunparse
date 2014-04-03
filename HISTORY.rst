=========
Changelog
=========

Here's the recent changes to AST Unparser.

.. changelog::
    :version: 1.2.0
    :released: 2014-04-03

    .. change::
        :tags: general

        Now compatible with Python 2.6 through Python 3.4.

    .. change::
        :tags: general

        A new function :func:`dump` is added to return a pretty-printed version
        of the AST. It's also available when running `python -m astunparse` as
        the `--dump` argument.


.. changelog::
    :version: 1.1.0
    :released: 2014-04-01

    .. change::
        :tags: general

        :func:`unparse` will return the source code for an AST. It is pretty
        feature-complete, and round-trips the stdlib, and is compatible with
        Python 2.7 and Python 3.4.

        Running `python -m astunparse` will print the round-tripped source for
        any python files given as argument.

