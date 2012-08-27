# coding: utf-8
__author__ = 'JB'

class ParseError(Exception):
    pass

properties = {'obj', 'key', 'attr', 'default', 'set', 'method'}
funcs = ['==', '=>', '=:', '=']

class OP:
    """ Possible operators for makeobj blocks
        == Equal to some other block
        => Key-value properties (multiline or not)
        =: Block structure
        =  Python data (multiline or not)
    """
    eq, kv, obj, py = funcs

class Info:
    """ Parsing status or content of element
    """
    close, open, data, line, end = 'close', 'open', 'data', 'line', 'end'
    #close, open, data, line, end = range(5)
