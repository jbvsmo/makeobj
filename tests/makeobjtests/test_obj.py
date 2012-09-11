# coding: utf-8
import unittest
import makeobj.obj as o

__author__ = 'JB'

class ObjTest(unittest.TestCase):

    def setUp(self):
        self.x = o.make('x', ['a', 'b', 'c'])
        self.y = o.make('y', zip([2,3,4], 'abc'))
        self.z = o.make(
            'z',
            {'a': {'num': 1},
             'b': {'num': 2},
             'c': {}},
            order=sorted,
            methods=
                {'f1': lambda self: self.name,
                 'f2': lambda self, val: self.value + val,
                 'f3': lambda self, *args: args},
            common_attr={'num': 0},
            doc='Example'
        )

    def test_names(self):
        x, y, z = self.x, self.y, self.z
        self.assertEqual(x.__name__, 'x')
        self.assertEqual(y.__name__, 'y')
        self.assertEqual(x.a.name, 'a')
        self.assertEqual(y.b.name, 'b')
        self.assertEqual(z.c.name, 'c')
        self.assertEqual(z.__doc__, 'Example')

    def test_values(self):
        x, y, z = self.x, self.y, self.z
        self.assertEqual(x.a.value, 0)
        self.assertEqual(x.b.value, 1)
        self.assertEqual(x.c.value, 2)
        self.assertEqual(y.a.value, 2)
        self.assertEqual(y.b.value, 3)
        self.assertEqual(y.c.value, 4)
        self.assertEqual(z.a.value, 0)
        self.assertEqual(z.b.value, 1)
        self.assertEqual(z.c.value, 2)

    def test_attr(self):
        z = self.z
        self.assertEqual(z.a.num, 1)
        self.assertEqual(z.b.num, 2)
        self.assertEqual(z.c.num, 0)

    def test_methods(self):
        z = self.z
        self.assertEqual(z.a.f1(), 'a')
        self.assertEqual(z.b.f2(5), 6)
        self.assertTupleEqual(z.c.f3(1, 2, 3), (1, 2, 3))

