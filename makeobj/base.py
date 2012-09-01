# coding: utf-8
from makeobj.obj import make_object

__author__ = 'JB'

class ParseError(Exception):
    pass

properties = set(('obj', 'key', 'attr', 'default', 'set', 'method'))
funcs = ['==', '=>', '=:', '=']

class OP:
    """ Possible operators for makeobj blocks
        == Equal to some other block
        => Key-value properties (multiline or not)
        =: Block structure
        =  Python data (multiline or not)
    """
    eq, kv, obj, py = funcs


# Parsing status or content of element
Info = make_object('Info', ['close', 'open', 'data', 'line', 'end'], common_attr={'line': None})
