# coding: utf-8

import unittest
import makeobj.tools as t

__author__ = 'JB'

class ToolsTest(unittest.TestCase):
    def test_min_max(self):

        self.assertEqual(t.max_([1,2,3]), 3)
        self.assertEqual(t.min_([1,2,3]), 1)

        self.assertEqual(t.max_([]), None)
        self.assertEqual(t.min_([]), None)

        self.assertEqual(t.max_([-1, -2, -3], key=abs), -3)
        self.assertEqual(t.min_([-1, -2, -3], key=abs), -1)

        self.assertEqual(t.max_([], key=abs, default=True), True)
        self.assertEqual(t.min_([], key=abs, default=True), True)

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
