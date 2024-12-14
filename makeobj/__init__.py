# coding: utf-8
"""
    makeobj - A tool to help building powerful enum classes
    Author: João Bernardo Oliveira - @jbvsmo
    License: BSD
"""

from .obj import make, Obj, no_conflict
from .helper import attr, class_attr, keys
from .text_parse_base import ParseError
from .text_parse import parse

__author__ = 'JB'
__all__ = ('parse', 'ParseError',
           'make', 'Obj', 'no_conflict',
           'attr', 'class_attr', 'keys',)

version = '0.9'


if __name__ == '__main__':
    pass
