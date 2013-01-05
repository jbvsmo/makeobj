# coding: utf-8
from distutils.core import setup
import makeobj

desc = '''
MakeObj is a module to help create powerful enumeration classes with support
to attributes specific for each element.

This module is compatible with Python versions 2.6+ and 3.0+

Usage:

>>> from makeobj import Obj, keys, attr
>>> class RGBColors(Obj):
...     red, green, blue = keys(3)
...     hex = attr('ff0000', '00ff00', '0000ff')
...
>>> RGBColors
<Object: RGBColors -> [red:0, green:1, blue:2]>
>>> RGBColors.red
<Value: RGBColors.red = 0>
>>> RGBColors.blue.hex
'0000ff'


Using the custom Enum Language:


::

  @obj RGBColors =:
      @keys = 'red', 'green', 'blue'
      @attr hex = 'ff0000', '00ff00', '0000ff'


Then you can parse it:

>>> from makeobj import parse
>>> RGBColors = parse(text)
>>> RGBColors.red
<Value: RGBColors.red = 0>

.
'''

setup(
    name = 'makeobj',
    version = makeobj.version,
    packages = ['makeobj'],
    url = 'https://github.com/jbvsmo/makeobj',
    license = 'BSD',
    author = 'João Bernardo Oliveira',
    author_email = 'jbvsmo@example.com',
    description = 'Powerful Enumeration System',
    long_description = desc,
    keywords = ['enum', 'enumeration', 'Enum Language'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
