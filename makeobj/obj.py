# coding: utf-8
__author__ = 'JB'
__metaclass__ = type

class __MetaObj(type):
    """ Metaclass for adding attributes and methods on the fly

        Do never use this metaclass directly. Inherit from the `Obj` class instead
    """
    _keys = {}      # Objects in the enum in {Num:Name} format
    _attr = {}      # Instance specific attributes
    _attrs = {}     # Attributes for all instances
    _meth = {}      # Mapping of methods to be set
    _methods = []   # Names of methods set in the class
    _names = ()     # Keys after possible tuple unpacking

    def __new__(mcs, name, bases, dic):
        """ A new metaclass (subclass of all bases!) is built and then created a new
            class to be later instantiated.
        """
        mcs = type(mcs.__name__ + ' > ' + name, tuple(type(i) for i in bases), dic)
        return type.__new__(mcs, name, bases, {})


    def __init__(cls, *args, **kw):
        type.__init__(cls,  *args, **kw)
        mcs = type(cls) #metaclass

        try:
            # See if cls._keys is made of key-value iterable
            # To allow the values to be chosen differently from range(X)
            _, _ = mcs._keys[0]
            try:
                _, _ = next(iter(mcs._attr))
            except (ValueError, IndexError, KeyError):
                pass
            else:
                # The attributes came in (num, name) format
                mcs._attr = dict((k, v) for (i,k),v in mcs._attr.items())

        except (ValueError, IndexError, KeyError):
            enum = enumerate(mcs._keys)
            # Get only the names in a set for fast check
            mcs._names = set(cls._keys)
        else:
            enum = mcs._keys
            # Get only the names in a set for fast check
            mcs._names = set(j for i,j in enum)
        mcs._keys = dict(enum)

        for k,v in mcs._meth.items():
            v.__name__ = k #just in case some lambdas reach here
            setattr(cls, k, v)
        mcs._methods = list(cls._methods)

        for i, name in mcs._keys.items():
            dic = {}
            dic.update(cls._attrs)
            dic.update(cls._attr.get(name, {}))

            setattr(mcs, name, cls._create(i, name, dic))

        mcs._attr.clear()
        mcs._attrs.clear()
        mcs._meth.clear()


    def __dir__(cls):
        """ Provide the members and methods names as metaclass attributes aren't shown by `dir`
            Also provide the _methods and _names attributes
        """
        return list(cls.__dict__) + ['_keys', '_methods', '_names'] + list(cls._names)

    def __repr__(cls):
        return '<Object: {0.__name__} -> [{1}]>'.format(cls, ', '.join(sorted(cls._names)))

    def __getitem__(cls, value):
        return cls(cls._keys[value])

    def _repr_pretty_(cls, p, cycle):
        """ IPython 0.13+ friendly representation for classes.
        """
        p.text(repr(cls))

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

class Obj:
    """ Base class without metaclass because of python 2.x/3.x
        incompatibilities. The metaclass is in the `Obj` class.
    """
    def __new__(cls, key):
        obj = getattr(cls, key, None)
        if obj is None:
            if key in cls._names:
                obj = object.__new__(cls)
            else:
                raise RuntimeError('Invalid name of object: %r' % key)
        return obj


    def __dir__(self):
        return list(self.__dict__) + list(type(self)._methods)

    def __repr__(self):
        return '<Value: {0.__name__}.{1._name} = {1._value} >'.format(type(self), self)

# Applying Metaclass compatible with both Python 2.x and 3.x
# Calling explicit type.__new__ is needed to avoid running MetaObj.__new__
Obj = type.__new__(__MetaObj, 'Obj', (Obj,), {})

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
    return {'_keys': [], '_attr': {}, '_attrs': {}, '_meth': {}}

def make_object_from_dict(name, data):
    """ Helper function to be used along with the `sample_dict` function.
        For simpler usage, refer to the `make` function.
    """
    return __MetaObj(name, (Obj,), data)

def make(name, keys, methods=None, common_attr=None, doc=''):
    """ Create a subclass of `Obj` with chosen elements, attributes and methods.

        name: The name of the resulting class.
        keys: All the instances this class will have.
              It may be a list or a dictionary with attributes for each instance.
              Example: ['inst1', 'inst2', 'inst3']
              Example: {'inst1': {'a': 1}, 'inst2': {'a': 2}}
              Also, the instances may be two item tuples with (value, name)
              Example: [(0, 'inst1'), (2, 'inst2'), (4, 'inst3')]
              Example: {(0, 'inst1'): {'a': 1}, (2, 'inst2'): {'a': 2}}
        methods: Functions to be added to the class that will become instance methods.
        common_attr: Attributes that have the same initial value to be added to all instances.
        doc: Text to document class
    """
    attr = {}
    if isinstance(keys, dict):
        attr = keys
        keys = list(keys)
    if methods is None:
        methods = {}
    if common_attr is None:
        common_attr = {}

    data = {'_keys': keys, '_attr': attr, '_meth': methods,
            '_attrs': common_attr, '__doc__': doc}
    return make_object_from_dict(name, data)
