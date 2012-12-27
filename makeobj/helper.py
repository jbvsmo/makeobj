# coding: utf-8
from makeobj.even_flow import *

__author__ = 'JB'
__all__ = ('attr', 'class_attr', 'keys')


ALLOWED_ENUM_TYPES = (int,)


class Modes(object):
    """ Special Modes
    """
    attr = 1
    common_attr = 2
    class_attr = 3
    keys = 4


class Special(object):
    """ Special attributes to retrieve elements on class definition.
        Do not use this class directly. Use the functions in this module.
    """
    def __init__(self, mode, **kw):
        self.mode = mode
        self.__dict__.update(kw)


def attr(*args, **kw):
    """ Attribute for all objects or attributes with default value that can
        be changed for individual elements.
            x = attr(1, 2, 3)
            y = attr(10, a=1, b=2)
    """
    if len(args) > 1 and kw:
        raise TypeError('Must supply either one default element and others by name '
                        'or multiple arguments arguments for all keys.\n'
                        'E.g.: attr(10, a=1, b=2) or attr(1, 2, 3)')

    if len(args) > 1:
        return Special(Modes.attr, elements=args)

    default = args[0] if args else None

    return Special(Modes.common_attr, default=default, elements=kw)


def keys(num, function=None):
    """ Return many keys to be unpacked into variables. They may have a
        function as value generator and a start value.
            a, b = keys(2)
            a, b, c = keys(3, lambda x: x**2)
    """
    if function is not None:
        val = [Special(Modes.keys, value=function(k))
               for k in range(num)]
    else:
        val = [Special(Modes.keys, value=None, pos=k)
               for k in range(num)]

    return val if num > 1 else val[0]


def class_attr(value):
    """ Class attribute that cannot be named the same as an element.
        Prefer using attr with default value when possible.
            x = class_attr(10)
    """
    return Special(Modes.class_attr, value=value)
