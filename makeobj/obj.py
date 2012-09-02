# coding: utf-8
__author__ = 'JB'
__metaclass__ = type

class __MetaObj(type):
    """ Metaclass for adding attributes and methods on the fly

        Do never create classes with this metaclass to avoid breaking it
    """
    _keys = ()      # Objects in the enum in {Num:Name} format
    _attr = {}      # Instance specific attributes
    _attrs = {}     # Attributes for all instances
    _methods = {}   # Methods set in the class
    _names = ()     # Keys after possible tuple unpacking

    def __init__(cls, *args, **kw):
        type.__init__(cls,  *args, **kw)
        metacls = type(cls)

        try:
            # See if cls._keys is made of key-value iterable
            # To allow the values to be chosen differently from range(X)
            _, _ = cls._keys[0]
        except (ValueError, IndexError):
            enum = enumerate(cls._keys)
            # Get only the names in a set for fast check
            metacls._names = set(cls._keys)
        else:
            enum = cls._keys
            # Get only the names in a set for fast check
            metacls._names = set(j for i,j in enum)
        metacls._keys = dict(enum)

        for k,v in cls._methods.items():
            v.__name__ = k #just in case some lambdas reach here
            setattr(cls, k, v)

        for i, name in metacls._keys.items():
            dic = {}
            dic.update(cls._attrs)
            dic.update(cls._attr.get(name, {}))

            setattr(metacls, name, cls._create(i, name, dic))

    def __dir__(cls):
        """ Provide the members and methods names as metaclass attributes aren't shown by `dir`
            Also provide the _methods and _names attributes
        """
        return list(cls.__dict__) + ['_keys', '_methods', '_names'] + list(cls._names)

    def __repr__(cls):
        return '<Object: {0.__name__} -> [{1}]>'.format(cls, ', '.join(sorted(cls._names)))

    def _create(cls, val, name, attr):
        """ Create instance from the class that will be set in the metaclass.
            The `value` and `name` atrributes have counterparts with `_` to
            allow these names to be overriten and still be available.
            This function also set all the instance attributes.
        """
        self = cls(name)
        self._value = self.value = val
        self._name = self.name = name
        for k,v in attr.items():
            setattr(self, k, v)
        return self

class __Obj:
    """ Base class without metaclass because of python 2.x/3.x
        incompatibilities. The metaclass is in the `Obj` class.

        Do never inherit from this class to avoid breaking it
    """
    def __new__(cls, key):
        if key in cls._names:
            obj = getattr(cls, key, None)
            if obj is None:
                return object.__new__(cls)
            return obj
        raise RuntimeError('Invalid name of object: %r' % key)

    #noinspection PyUnusedLocal
    def __init__(self, key):
        pass

    def __dir__(self):
        return list(self.__dict__) + list(type(self)._methods)

    def __repr__(self):
        return '<Value: {0.__name__}.{1._name} = {1._value} >'.format(type(self), self)

# Applying Metaclass compatible with both Python 2.x and 3.x
# Useful for direct subclassing Obj without `make_object`.
__Obj = __MetaObj('__Obj', (__Obj,), {})

class MicroObj:
    """ Small Objects to be used like a dictionary but with `getattr` syntax
        instead of `getitem`.
    """
    def __init__(self, data=None):
        if data is not None:
            self.__dict__.update(data)

    def __repr__(self):
        return '<MicroObj: [{0}]>'.format(', '.join(sorted(self.__dict__)))

def sample_dict():
    """ Create the basic layout of attributes needed to create a new class.
    """
    return {'_keys': [], '_attr': {}, '_attrs': {}, '_methods': {}}

def make_object_from_dict(name, data):
    """ Helper function to be used along with the `sample_dict` function.
        For simpler usage, refer to the `make_object` function.
    """
    meta = type('_SubMetaObj', (__MetaObj,), data)
    return meta(name, (__Obj,), {})

def make_object(name, keys, attr=None, methods=None, common_attr=None, doc=''):
    """ Create a subclass of `Obj` with chosen elements, attributes and methods.

        name: The name of the resulting class.
        keys: All the instances this class will have.
        attr: Dictionary with attributes for each instance.
              Example: {'inst1': {'a': 1}, 'inst2': {'a': 2}}
        methods: Functions to be added to the class that will become instance methods.
        common_attr: Attributes that have the same initial value to be added to all instances.
        doc: Text to document class
    """
    if attr is None:
        attr = {}
    if methods is None:
        methods = {}
    if common_attr is None:
        common_attr = {}

    data = {'_keys': keys, '_attr': attr, '_methods': methods,
            '_attrs': common_attr, '__doc__': doc}
    return make_object_from_dict(name, data)