# coding: utf-8
from distutils.core import setup
import makeobj

desc = '''
MakeObj is a module to help create powerful enumeration classes with support
to attributes specific for each element.

This module is compatible with Python versions 2.6+ and 3.0+
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
    long_description=desc,
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
