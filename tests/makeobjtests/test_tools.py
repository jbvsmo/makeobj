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
