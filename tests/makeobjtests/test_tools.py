# coding: utf-8

import unittest
import types
from makeobj.even_flow import *
from makeobj import tools as t

__author__ = 'JB'

class ToolsTest(unittest.TestCase):
    def test_min_max(self):

        self.assertEqual(t.max([1,2,3]), 3)
        self.assertEqual(t.min([1,2,3]), 1)

        self.assertEqual(t.max([]), None)
        self.assertEqual(t.min([]), None)

        self.assertEqual(t.max([-1, -2, -3], key=abs), -3)
        self.assertEqual(t.min([-1, -2, -3], key=abs), -1)

        self.assertEqual(t.max([], key=abs, default=True), True)
        self.assertEqual(t.min([], key=abs, default=True), True)

    def test_iter_items(self):

        def it(*args, **kw):
            return list(t.iter_items(*args, **kw))

        x = (1, 2, 3, 4)
        y = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

        final = sorted(y.items())

        self.assertEqual(it(x, 'abcd'), final)
        self.assertEqual(it(x, 'abc'), final[:-1])

        self.assertEqual(it(y, 'abcd'), final)
        self.assertEqual(it(y, 'abc'), final[:-1])

    def test_no_unbound_stuff(self):

        class C(object):
            def f(self):
                pass

            @t.NoUnbound
            def g(self):
                pass

            @t.no_unbound
            def h(self):
                pass

        if v3:
            self.assertEqual(type(C.f), types.FunctionType)
        else:
            self.assertNotEqual(type(C.f), types.FunctionType)

        self.assertEqual(type(C.g), types.FunctionType)
        self.assertEqual(type(C.h), types.FunctionType)
