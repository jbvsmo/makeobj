# coding: utf-8
import collections
import types
from .helper import Modes, Special, ALLOWED_ENUM_TYPES
from .even_flow import *
from . import tools

__author__ = 'JB'


def fix_dict(dic):
    """ Modify a dictionary to make it conformant with `obj.sample_dict`
        Change
    """
    _keys = list(dic.pop('_keys', []))
    _attr = dic.pop('_attr', {})

    special = [(k, v) for k, v in dic.items() if isinstance(v, Special)]
    for k, v in special:
        dic.pop(k)

    keys = [(k, v) for k, v in special if v.mode == Modes.keys]
    attr = [(k, v) for k, v in special if v.mode in (Modes.attr, Modes.common_attr)]
    class_attr = [(k, v.value) for k, v in special if v.mode == Modes.class_attr]

    keys_type = [(k, v) for k, v in dic.items() if isinstance(v, ALLOWED_ENUM_TYPES)]
    for k, v in keys_type:
        dic.pop(k)

    funcs = [(k, v) for k, v in dic.items() if isinstance(v, types.FunctionType)]
    for k, v in funcs:
        dic.pop(k)

    # TODO - Make SubObj useful!
    #subobj = [(k, v) for k, v in dic.items() if isinstance(v, obj.SubObj)]
    #for k, v in subobj:
    #    dic.pop(k)

    dic.update(class_attr)
    dic['_keys'], keys = _fix_keys(keys, _keys, keys_type)
    dic['_attr'] = _fix_attr(attr, _attr, keys)

    dic.setdefault('_meth', {}).update(funcs)

    # Unused things are left in the dictionary without changes
    return dic


def _fix_keys(keys, _keys, keys_type):
    """ Fix the keys together.
        Join keys made of Special objects with "ready keys" and
        keys made of elements of allowed types.

        Will return the final "ready keys" and their names
    """
    final_keys = []

    all_tuples = all(len(x) == 2 for x in _keys)
    no_tuples = all(isinstance(x, str) for x in _keys)

    no_values = all(v.value is None for k, v in keys)
    all_values = all(v.value is not None for k, v in keys)

    error_mixed = False
    keys_names = []
    if all_tuples and all_values:
        final_keys = [(v.value, k) for k, v in keys] + _keys + \
                     [(v, k) for k, v in keys_type]
        final_keys.sort()
        keys_names = [v for k, v in final_keys]
    elif keys_type:
        error_mixed = True
    elif no_values and no_tuples:
        keys.sort(key=lambda x: x[1].pos)
        final_keys = [k for k, v in keys] + _keys
        keys_names = final_keys
    else:
        error_mixed = True

    if error_mixed:
        raise TypeError('Either all keys have their values defined or none '
                        'of them can have.')

    return final_keys, keys_names


def _fix_attr(attr, _attr, keys):
    """ Fix the elements attributes together.
    """
    out = collections.defaultdict(dict)
    out.update(_attr)

    for name, v in attr:
        if v.mode == Modes.common_attr:
            for k in keys:
                out[k][name] = v.elements.get(k, v.default)
        else:
            for k, el in zip(keys, v.elements):
                out[k][name] = el

    return dict(out)


def _check_bases(bases):
    """ Check for repeated names or keys on base classes.
    """
    if len(bases) == 1:
        return

    names = tools.flat(b._names for b in bases)
    try:
        dup = tools.duplicate(names)
    except ValueError:
        pass
    else:
        raise TypeError('Duplicated enum name on parent classes: %r' % dup)

    values = tools.flat(b._keys for b in bases)
    try:
        dup = tools.duplicate(values)
    except ValueError:
        pass
    else:
        raise TypeError('Duplicated enum value on parent classes: %s' % dup)
