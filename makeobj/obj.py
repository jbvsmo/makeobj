# coding: utf-8
__author__ = 'JB'
__metaclass__ = type


class MetaObj(type):
    """ Metaclass for adding attributes and methods on the fly
    """
    _keys = ()      # Objects in the enum
    _attr = {}      # Instance specific attributes
    _attrs = {}     # Attributes for all instances
    _methods = {}   # Methods set in the class

    def __init__(cls, *args, **kw):
        super(MetaObj, cls).__init__(*args, **kw)

        try:
            # See if cls._keys is made of key-value iterable
            # To allow the values to be chosen differently from range(X)
            _, _ = cls._keys[0]
        except (ValueError, IndexError):
            enum = enumerate(cls._keys)
            # Get only the names in a set for fast check
            cls._names = set(cls._keys)
        else:
            enum = cls._keys
            # Get only the names in a set for fast check
            cls._names = set(j for i,j in enum)

        for k,v in cls._methods.items():
            v.__name__ = k #just in case some lambdas reach here
            setattr(cls, k, v)

        for i, name in enum:
            dic = cls._attr.get(name, {})
            dic.update(cls._attrs)
            setattr(cls, name, cls._create(i, name, dic))

    def __repr__(cls):
        return '<Object: {0.__name__} -> [{1}]>'.format(cls, ' '.join(sorted(cls._names)))

    def _create(cls, val, name, attr):
        self = cls(name)
        self._value = val
        self._name = name
        for k,v in attr.items():
            setattr(self, k, v)
        return self

class Obj:
    """ Base class without metaclass because of python 2.x/3.x
        incompatibilities. The metaclass is in the `Obj` class.
    """
    def __new__(cls, key):
        if key in cls._names:
            obj = getattr(cls, key, None)
            if obj is None:
                return object.__new__(cls)
            return obj
        raise RuntimeError('Invalid name of object: %r' % key)

    def __repr__(self):
        return '<Value: {0.__name__}.{1._name} = {1._value} >'.format(type(self), self)

# Applying Metaclass compatible with both Python 2.x and 3.x
# Useful for direct subclassing Obj without `make_object`
Obj = MetaObj('Obj', (Obj,), {})


def make_object(name, keys, attr=None, methods=None, class_attr=None):
    """ Create a subclass of `Obj` with chosen elements, attributes and methods.
    """
    if attr is None:
        attr = {}
    if methods is None:
        methods = {}
    if class_attr is None:
        class_attr = {}

    data = {'_keys': keys, '_attr': attr, '_methods': methods, '_attrs': class_attr}
    return MetaObj(name, (Obj,), data)

