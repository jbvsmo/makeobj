# coding: utf-8
"""
    makeobj - A tool to help building powerful enum classes
    Author: João Bernardo Oliveira - @jbvsmo
    License: BSD
"""

#noinspection PyUnresolvedReferences
from makeobj.base import ParseError
from makeobj.obj import make
from makeobj.text_parse import _parse, _iter_parse, _build_all

__author__ = 'JB'
__metaclass__ = type
__all__ = ('parse', 'ParseError', 'make')

version = '0.1'

def parse(text, upto=None):
    """ Parse a block of text in makeobj format and create a list of elements
        Works with file handlers, multiline strings and other iterables
        The second argument can make the text parsing stop in a certain line if given.
    """
    if not hasattr(text, 'readlines'):
        try:
            text = text.splitlines()
        except AttributeError:
            pass # treat as an iterable of lines

    objs = _build_all(_parse(_iter_parse(text, upto)))
    if not objs:
        raise ParseError('No object found!')
    return objs[0] if len(objs) == 1 else objs


if __name__ == '__main__':
    pass
