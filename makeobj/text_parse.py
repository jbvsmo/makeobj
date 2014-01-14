# coding: utf-8
import ast
import re
import itertools
from .text_parse_base import funcs, ParseError, Info, OP, Prop
from .obj import sample_dict, make_object_from_dict, SubObj

__author__ = 'JB'
__metaclass__ = type

_re_comand = re.compile(r'^@(\w+)\s*(?::?\s*(\w+))?\s*(' + '|'.join(funcs) + ')\s*(.*)$')


def parse(text, upto=None):
    """ Parse a block of text in makeobj format and create a list of elements
        Works with file handlers, multiline strings and other iterables
        The second argument can make the text parsing stop in a certain line if given.
    """
    if not hasattr(text, 'readlines'):
        try:
            text = text.splitlines()
        except AttributeError:
            pass  # Treat as an iterable of lines

    objs = _build_all(*_parse(_iter_parse(text, upto)))
    if not objs:
        raise ParseError('No object found!')
    return objs[0] if len(objs) == 1 else objs


def _indent(line):
    """ Return indentation size and the line whithout identation and
        trailing whitespace
    """
    new = line.lstrip()
    return len(line) - len(new), new.rstrip()


def _break_line(line):
    """ Split a block opening line using regex or raise an error on
        normal lines
    """
    return _re_comand.findall(line)[0]


def _iter_parse(text, upto=None):
    """ Iterate over lines, and take care of blocks and indentation levels.
        Also split the information of block opening lines.
    """
    increase_indent = False
    indent_history = []
    for cnt, line in enumerate(text, 1):
        if upto is not None and upto == cnt:
            break

        i, line = _indent(line)
        if not line or line.startswith('#'):
            continue

        if not indent_history:
            # The first indentation level is the smallest acceptable.
            indent_history.append(i)

        old = indent_history[-1]
        if i < old:
            if increase_indent:
                ParseError('Expected an indented block. Line %s' % cnt)
            while i != old:
                yield None, Info.close  # End of block

                indent_history.pop()
                if not indent_history:
                    raise ParseError('Unindent does not match any parent level. Line %s' % cnt)
                old = indent_history[-1]
        if i > old:
            if not increase_indent:
                raise ParseError('Unexpect indentation. Line %s' % cnt)
            indent_history.append(i)
            yield None, Info.open  # Start of new block

        try:
            data = _break_line(line)
            increase_indent = not data[-1]
            yield data, Info.data  # Block of only one line with Python data

        except IndexError:
            increase_indent = False
            yield line, Info.line  # Line of Python data

    yield None, Info.end  # End of file. Should work the same way as Info.close


def _load_block(iterator, op):
    """ Load a data block until it reaches its close or end tag.
        It can return a list after each line is evaluated to Python data
        or a dictionary after each line is evaluated as key:value pair
        depending on the `op` (operator) inputed.
    """
    if next(iterator)[1] is not Info.open:
        raise ParseError("Missing Block!")
    data = itertools.takewhile(lambda x: x[1] is Info.line, iterator)
    if op == OP.py:
        #multiline list
        return [ast.literal_eval(x[0]) for x in data]
    else:
        #multiline dict
        return ast.literal_eval('{%s}' % ','.join(x[0] for x in data))


def _parse(it):
    """ Do the real recursive parsing that allow blocks inside blocks
        by running on top of `_iter_parse` iterator.
    """
    data = {}
    order = []  # top-level objects must be in the right order
    for i, j in it:
        if j in (Info.close, Info.end):
            return data, order
        if j is Info.data:
            prop, name, op, val = i
            prop = Prop(prop)
            if not name:
                name = '@' + prop.name
            if op != OP.eq:
                if op != OP.obj:  # There's not a sub object (new block)
                    val = ast.literal_eval(val if op == OP.py else '{%s}' % val) \
                        if val \
                        else _load_block(it, op)
                else:
                    if val:
                        val = ast.literal_eval(val)
                        prop = Prop.default
                    else:
                        val, _ = _parse(it)
            else:
                pass  # TODO missing the value conversion for OP.eq
            if name not in data:
                order.append(name)
            data[name] = prop(val)
    return data, order


def _build_all(data, order):
    return [_build(el, data[el]) for el in order]


def _build(name, obj, dic=None, keys=None):
    """ Parse dictionaries of `PropObj` elements
    """
    # OBJ
    if obj.mode is Prop.obj:
        dic = sample_dict()
        data = obj.value
        keys = dic['_keys'] = data.pop('@keys').value
        for nm, val in data.items():
            _build(nm, val, dic, keys)
            #return {name: dic}
        return make_object_from_dict(name, dic)

    # SUB
    elif obj.mode is Prop.sub:
        sdic = sample_dict()
        data = obj.value
        for nm, val in data.items():
            _build(nm, val, sdic, keys)

        for k in keys:
            attr = {}
            attr.update(sdic['_attrs'])
            attr.update(sdic['_meth'])
            attr.update(sdic['_attr'].get(k, {}))

            dic['_attr'].setdefault(k, {})[name] = SubObj(attr)

    # ATTR
    elif obj.mode is Prop.attr:
        if isinstance(obj.value, dict):
            for v in obj.value.values():
                _build(name, v, dic, keys)
        else:
            for k, v in zip(keys, obj.value):
                dic['_attr'].setdefault(k, {})[name] = v

    # SET
    elif obj.mode is Prop.set:
        for k, v in obj.value.items():
            dic['_attr'].setdefault(k, {})[name] = v

    # DEFAULT
    elif obj.mode is Prop.default:
        dic['_attrs'][name] = obj.value

    # METHOD
    elif obj.mode is Prop.method:
        dic['_meth'][name] = lambda self=None, *args, **kw: obj.value  # TODO Fix lambdas state

    # ERROR!
    else:
        #print("ERROR", name, obj)
        raise ParseError('Invalid Property', name)
