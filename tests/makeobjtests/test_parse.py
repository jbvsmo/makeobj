# coding: utf-8
import unittest
import os
import makeobj

__author__ = 'JB'

test_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_file(name):
    with open(os.path.join(test_root, 'files', name + '.makeobj')) as f:
        return makeobj.parse(f)


class ParseTest(unittest.TestCase):
    """ Test parsing tool with example files.
    """

    def test_all(self):
        A = parse_file('f1')

        self.assertEqual(A.__name__, 'StatusProblems')
        self.assertEqual(A.ok.name, 'ok')
        self.assertEqual(A.burn._name, 'burn')
        self.assertEqual(A.sleep.value, A.sleep._value)
        self.assertEqual(A.freeze.abrev, 'FRZ')
        self.assertAlmostEqual(A.paralyze.bonus, 1.5)
        self.assertAlmostEqual(A.burn.damage, 0.125)
        self.assertAlmostEqual(A.sleep.damage, 0)
        self.assertEqual(A.poison.walkloss, True)
        self.assertEqual(A.ok.walkloss, False)
        self.assertAlmostEqual(A.freeze.move.chance, 0)
        self.assertAlmostEqual(A.paralyze.move.chance, 0.5)
        self.assertAlmostEqual(A.burn.move.chance, 1)
        self.assertEqual(A.ok.foo(), 123)

    def test_deep(self):
        A = parse_file('f2')

        self.assertEqual(A.a.a0, 'a')
        self.assertEqual(A.a.a1, 'b')
        self.assertEqual(A.b.x.a2, 'c')
        self.assertEqual(A.b.x.a3, 'd')
        self.assertEqual(A.c.x.y.a4, 'e')
        self.assertEqual(A.c.x.y.a5, 'f')
        self.assertEqual(A.a.x.y.z.a6, 'g')

        self.assertEqual(A.b.m0(), 0)
        self.assertEqual(A.c.x.m1(), 1)
        self.assertEqual(A.a.x.y.m2(), 2)
        self.assertEqual(A.b.x.y.z.m3(), 3)

    def test_eq_obj(self):
        A = parse_file('f3')
        n = 1

        self.assertEqual(A.a.x, n)
        self.assertEqual(A.b.x, n)
        self.assertEqual(A.c.x, n)
        self.assertEqual(A.a.y, n)
        self.assertEqual(A.b.y, n)
        self.assertEqual(A.c.y, n)

    def test_multiline_strings(self):
        # This multiline string starts at an indentation level
        # bigger than 0. This should be accepted!
        t = '''
        @obj: A =:
            @keys = 'a', 'b', 'c'
            @attr: x =: 1
        '''

        A = makeobj.parse(t)
        self.assertEqual(A.__name__, 'A')
        self.assertEqual(A.a.value, 0)
        self.assertEqual(A.b.x, 1)
        self.assertEqual(A.c.name, 'c')

    def test_order(self):
        t = '''
        @obj A =:
            @keys = 'a', 'b'

        @obj B =:
            @keys = 'a', 'b'

        @obj C =:
            @keys = 'a', 'b'

        @obj D =:
            @keys = 'a', 'b'

        @obj F =:
            @keys = 'a', 'b'

        @obj E =:
            @keys = 'a', 'b'
        '''

        objs = makeobj.parse(t)
        names = ''.join(x.__name__ for x in objs)
        self.assertEqual(names, 'ABCDFE')