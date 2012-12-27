# coding: utf-8
import collections
from makeobj.even_flow import *

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


def min_(iterable, key=None, default=None):
    """ Use a default value when it's not possible to get
        the min value of an iterable (e.g. empty sequence)
    """
    return default_min_max(iterable, key, default, min)


def max_(iterable, key=None, default=None):
    """ Use a default value when it's not possible to get
        the max value of an iterable (e.g. empty sequence)
    """
    return default_min_max(iterable, key, default, max)


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
