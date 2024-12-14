# coding: utf-8
""" Try to make program flow to be similar on Python 2 and Python 3
    Should be used as `from even_flow import *`
"""

__author__ = 'JB'

import sys as _sys
import itertools as _it
import collections as _collections
try:
    import builtins
except ImportError:
    import __builtin__ as builtins

v2 = _sys.version_info[0] == 2

if not v2:
    basestring = str
    long = int
    cmp = lambda first, second: NotImplemented

    if not hasattr(builtins, 'callable'):
        def callable(object):
            return isinstance(object, _collections.Callable)

    if not hasattr(_collections, 'Mapping'):
        import collections.abc as _abc
        _collections.Mapping = _abc.Mapping
else:
    zip = _it.izip
    map = _it.imap
    filter = _it.ifilter
    range = xrange
