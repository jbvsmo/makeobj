# coding: utf-8
from distutils.core import setup
import makeobj

setup(
    name = 'makeobj',
    version = makeobj.version,
    packages = ['makeobj'],
    url = 'https://github.com/jbvsmo/makeobj',
    license = 'BSD',
    author = 'João Bernardo Oliveira',
    author_email = 'jbvsmo@example.com',
    description = 'Powerful Enumeration System',
    classifiers = [
        'Development Status :: 3 - Alpha',
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
