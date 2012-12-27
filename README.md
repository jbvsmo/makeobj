MakeObj - Powerful Enumeration System
=====================================

* Author:    João Bernardo Oliveira ([@jbvsmo](http://twitter.com/jbvsmo))
* Version:   0.6
* GitHub:    <https://github.com/jbvsmo/makeobj>

MakeObj is a module to help create powerful enumeration classes with support
to attributes specific for each element.

This module is compatible with Python versions 2.6+ and 3.0+

Using it
========

MakeObj lets you create enumerations with a simple language like that:

```python
@obj: RGBColors =:
    @keys = 'red', 'green', 'blue'

    @attr: hex = 'ff0000', '00ff00', '0000ff'

    @attr: is_nice =:
        @default = False
        @set => 'blue': True
```

Then you can use like this:

```python
RGBColors = makeobj.parse(text)

if RGBColors.blue.is_nice:
    print('I like blue')

print('The hex value of {0.name} is #{0.hex}'.format(RGBColors.red))
```


If you have simple enums, you can use like this:

```python
RGBColors = makeobj.make('RGBColors', ['red', 'green', 'blue'])
```

or, with some more data, one may want to write a class:

```python
class RGBColors(Obj):
    red, green, blue = keys(3)
    hex = attr('ff0000', '00ff00', '0000ff')

```

Status
======

This project is in test stage and some issues are expected mainly in the parsing language.
It will parse conformant code, but still may not show all the errors and may load an invalid
file skipping some data when it should raise an error.

The `make` function works fine but it may be easier to write a class instead. The
`SubObj` machinery (see the `tests/files` directory for examples) only works in
the Enum Language. Yet!


Features
========

 * Enumerations with simple attributes, methods or even small objects with their own attributes.
 * An Enumeration Language for easy creation of objects.
 * The enumeration by default use the values 0 to N-1 but you may specify your own values.
 * The elements of the class are really instances of it and can take advantage of the `isinstance`
   function. Because of a metaclass factory, the classes do not share unwanted attributes with
   the instances.
 * The elements come with two attributes by default: `name` and `value` (also `_name` and `_value`
   in case you want to override them).
 * Elements can (and should!) be checked with the `is` comparison and can be retrieved by name in string
   form or value from their class: `RGBColors('red')` or `RGBColors[0]` or `RGBColors.red` result in the
   same object.
 * Enum values must be integer for simplicity and to help usability.
 * Subclassing is great!

TODO
====

 * Finalize the specs of MakeObj Enum Language v1.0.
 * Change the `@method` property to allow better function/method support
 * Create a helper function to load a directory of `.makeobj` files as they
   were a python module.
 * Better suport on subclassing: multiple inheritance, parent default attributes