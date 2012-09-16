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
        self.assertEqual(z._methods, ['f1', 'f2', 'f3'])
        self.assertEqual(z.a.f1(), 'a')
        self.assertEqual(z.b.f2(5), 6)
        self.assertEqual(z.c.f3(1, 2, 3), (1, 2, 3))

    def test_build_class_simple(self):
        class X(o.Obj):
            _keys = 'a', 'b'
            _attr = {'a': {'x': 1, 'y': 2},
                     'b': {'x': 2}}
            _attrs = {'y': 0}

        self.assertEqual(X.a.value, 0)
        self.assertEqual(X.b.value, 1)
        self.assertEqual(X.a.x, 1)
        self.assertEqual(X.b.x, 2)
        self.assertEqual(X.a.y, 2)
        self.assertEqual(X.b.y, 0)

    def test_build_class_complex(self):
        class X(o.Obj):
            _keys = (1, 'a'), (3, 'b')
            _attr = {'a': {'x': 1},
                     'b': {'x': 2}}

        class Y(o.Obj):
            _keys = (1, 'a'), (3, 'b')
            _attr = {(1, 'a'): {'x': 1},
                     (3, 'b'): {'x': 2}}

        class Z(o.Obj):
            _keys = (1, 'a'), (3, 'b')
            _attr = {(0, 'a'): {'x': 1},
                     (0, 'b'): {'x': 2}}

        self.assertEqual(X.a.value, 1)
        self.assertEqual(X.b.value, 3)
        self.assertEqual(Y.a.value, 1)
        self.assertEqual(Y.b.value, 3)
        self.assertEqual(Z.a.value, 1)
        self.assertEqual(Z.b.value, 3)

        self.assertEqual(X.a.x, 1)
        self.assertEqual(Y.b.x, 2)
        self.assertEqual(Z.a.x, 1)

    def test_subclass(self):
        class X(o.Obj):
            _keys = 'a', 'b'
            test = 1

        class Y(X):
            pass

        class Z(Y):
            _keys = 'c',

        self.assertEqual(X._names, Y._names)
        self.assertEqual(X._names.union('c'), Z._names)
        self.assertEqual(X.a, Y.a)
        self.assertEqual(Y.b, Z.b)
        self.assertEqual(X.test, Z.test)

    def test_repeated_value(self):
        f = lambda : o.make('test', [(0,'a'), (1, 'b'), (1, 'c')])
        self.assertRaises(RuntimeError, f)