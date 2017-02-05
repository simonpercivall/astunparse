# coding: utf-8
from __future__ import absolute_import
from six.moves import cStringIO
from .unparser import Unparser
from .printer import Printer


__version__ = '1.5.0'


def unparse(tree):
    v = cStringIO()
    Unparser(tree, file=v)
    return v.getvalue()


def dump(tree):
    v = cStringIO()
    Printer(file=v).visit(tree)
    return v.getvalue()
