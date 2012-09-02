# coding: utf-8
from makeobj.obj import make_object

__author__ = 'JB'
__metaclas__ = type

class ParseError(Exception):
    pass

funcs = ['==', '=>', '=:', '=']

class OP:
    """ Possible operators for makeobj blocks
        == Equal to some other block
        => Key-value properties (multiline or not)
        =: Block structure
        =  Python data (multiline or not)
    """
    eq, kv, obj, py = funcs


doc = """ Parsing status or content of element """
Info = make_object('Info', ['close', 'open', 'data', 'line', 'end'],
                   common_attr={'line': None}, doc=doc)


class PropObj:
    """ Object to hold property elements
    """
    def __init__(self, mode, value):
        self.mode = mode
        self.value = value
    def __repr__(self):
        return '<{0.mode}: {0.value}>'.format(self)

def prop_call(self, value):
    """ Create a new PropObj with the call syntax for the prop object
    """
    return PropObj(self, value)

doc = """ Possible properties for objects """
Prop = make_object('Prop', ['obj', 'keys', 'attr', 'default', 'set', 'method', 'sub'],
                   methods={'__call__': prop_call}, doc=doc)