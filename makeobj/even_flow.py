# coding: utf-8
""" Try to make program flow to be similar on Python 2 and Python 3
"""

__author__ = 'JB'

import sys
import itertools
try:
    import builtins as _btn
except ImportError:
    import __builtin__ as _btn

v3 = sys.version_info[0] == 3

if not v3:
    zip = itertools.izip
else:
    zip = _btn.zip
