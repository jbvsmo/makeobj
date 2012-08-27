# coding: utf-8
"""
    makeobj - A tool to help building powerful enum classes
    Author: João Bernardo Oliveira - @jbvsmo
    License: BSD
"""

from makeobj.text_parse import _parse, _iter_parse

__author__ = 'JB'
__metaclass__ = type


def parse(text, upto=None):
    """ Parse a block of text in makeobj format and create a list of elements
        Works with file handlers, multiline strings and other iterables
    """
    if not hasattr(text, 'readlines'):
        try:
            text = text.splitlines()
        except AttributeError:
            pass # treat as an iterable of lines

    return _parse(_iter_parse(text, upto))


if __name__ == '__main__':
    print(parse(open('../tests/f1.makeobj')))