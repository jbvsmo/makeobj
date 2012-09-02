# coding: utf-8
"""
    makeobj - A tool to help building powerful enum classes
    Author: João Bernardo Oliveira - @jbvsmo
    License: BSD
"""

#noinspection PyUnresolvedReferences
from makeobj.obj import make_object
from makeobj.text_parse import _parse, _iter_parse, _build_all

__author__ = 'JB'
__metaclass__ = type
__all__ = ('parse', 'make_object')


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

    return _build_all(_parse(_iter_parse(text, upto)))


if __name__ == '__main__':
    import pprint
    pprint.pprint(parse(open('../tests/f1.makeobj')))
    #pprint.pprint(parse(open(r'E:\Dropbox\dev\poke\mon\info\stats.makeobj')))