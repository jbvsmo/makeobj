# coding: utf-8
import collections
import types
from .even_flow import *

__author__ = 'JB'


def default_min_max(iterable, key, default, fn):
    """ Use a default value when it's not possible to get
        the min/max value of an iterable (e.g. empty sequence)
    """
    try:
        if key is None:
            return fn(iterable)
        else:
            return fn(iterable, key=key)
    except ValueError:
        return default


def min(iterable, key=None, default=None):
    """ Use a default value when it's not possible to get
        the min value of an iterable (e.g. empty sequence)
    """
    return default_min_max(iterable, key, default, builtins.min)


def max(iterable, key=None, default=None):
    """ Use a default value when it's not possible to get
        the max value of an iterable (e.g. empty sequence)
    """
    return default_min_max(iterable, key, default, builtins.max)


def iter_items(iterable, keys):
    """ Make iteration on dictionaries and lists even
        The user will supply a list of keys
    """
    if isinstance(iterable, collections.Mapping):
        for k in keys:
            yield k, iterable[k]
        return
    for k, v in zip(keys, iterable):
        yield k, v


class NoUnbound(object):
    """ Decorator to mimic Python 3.x default behavior on function __get__
        at class level. No more `unbound method`.
    """
    def __init__(self, function):
        self._function = function
    def __get__(self, instance, owner):
        fn = self._function
        if instance is None:
            return fn
        return type(fn).__get__(fn, instance, owner)


def no_unbound(function):
    """ Make a function a NoUnbound object by first checking the type.
    """
    if isinstance(function, types.FunctionType):
        return NoUnbound(function)
    return function