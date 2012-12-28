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

v3 = _sys.version_info[0] == 3

if v3:
    basestring = str
    long = int
    if not hasattr(builtins, 'callable'):
        def callable(object):
            return isinstance(object, _collections.Callable)
else:
    zip = _it.izip
    map = _it.imap
    filter = _it.ifilter
    range = xrange
