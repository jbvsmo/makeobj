# coding: utf-8
import unittest
from makeobj.helper import class_attr, attr, keys
from makeobj.even_flow import *
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

    def test_repeated_value(self):
        f = lambda : o.make('test', [(0,'a'), (1, 'b'), (1, 'c')])
        self.assertRaises(RuntimeError, f)

    def test_iterate(self):
        class A(o.Obj):
            a, b = keys(2)
        class B(A):
            c, d = keys(2)

        self.assertEqual(list(A), [A.a, A.b])
        self.assertEqual(tuple(B), (B.a, B.b, B.c, B.d))

class ObjTestComparison(unittest.TestCase):

    def setUp(self):
        class A(o.Obj):
            a, b = keys(2)
        class B(o.Obj):
            a, b = keys(2)
        class C(A):
            c, d = keys(2)

        self.cls = A, B, C

    def test_lt_le_gt_ge(self):
        A, B, C = self.cls

        self.assert_(A.a < C.c)
        self.assert_(C.c > A.a)
        self.assert_(A.b <= C.d)
        self.assert_(C.d >= A.b)
        self.assertRaises(TypeError, lambda: A.a < B.b)
        self.assertRaises(TypeError, lambda: A.a > B.b)
        self.assertRaises(TypeError, lambda: B.a <= A.b)
        self.assertRaises(TypeError, lambda: B.b >= A.a)

    def test_eq_ne(self):
        A, B, C = self.cls

        self.assertEqual(A.a, C.a)
        self.assertEqual(C.b, A.b)
        self.assertNotEqual(A.a, B.a)
        self.assertNotEqual(B.b, C.b)

        if not v3:
            # Do not allow old style comparisons
            self.assertRaises(TypeError, cmp, A.a, B.a)
            self.assertRaises(TypeError, cmp, B.b, A.b)

    def test_sort(self):
        A, B, C = self.cls

        self.assertEquals(sorted([C.b, C.d, C.a, C.c]),
                                 [C.a, C.b, C.c, C.d])

        self.assertEquals(sorted([C.b, C.d, C.a, C.c], reverse=1),
                                 [C.d, C.c, C.b, C.a])


class ObjTestSubclass(unittest.TestCase):

    def setUp(self):
        class X(o.Obj):
            a, b = keys(2)
            n1 = class_attr(1)
            n2 = attr(10)

        class Y(X):
            pass

        class Z(Y):
            c = 2

            def f(self):
                return self.value + 1

        class W(Z):
            _keys = (3, 'd'),

        class X1(X):
            c = keys(1)

        class X2(X1):
            d, e = keys(2)

        self.cls = X, Y, Z, W, X1, X2

    def test_subclass_values(self):
        X, Y, Z, W, X1, X2 = self.cls

        self.assertEqual(X.a, X[0])
        self.assertEqual(Y.b.value, 1)
        self.assertEqual(Z.c, Z[2])
        self.assertEqual(W.d.value, 3)

        self.assertEqual(X2.a, X2[0])
        self.assertEqual(X1.b.value, 1)
        self.assertEqual(X1.c, X1[2])
        self.assertEqual(X2.d.value, 3)
        self.assertEqual(X2.e, X2[4])

    def test_subclass_simple(self):
        X, Y, Z = self.cls[:3]

        self.assertEqual(X._names, Y._names)
        self.assertEqual(X._names.union('c'), Z._names)
        self.assertEqual(X.a, Y.a)
        self.assertEqual(Y.b, Z.b)
        self.assertEqual(X.n1, Z.n1)

    def test_subclass_get_item(self):
        X, Y, Z, W = self.cls[:4]

        self.assertEqual(X[0], Y[0])
        self.assertEqual(Y[1], Z[1])
        self.assertEqual(Z[0], X[0])
        self.assertEqual(Z[0], X[0])
        self.assertEqual(Z[2], W[2])
        self.assertEqual(W[1], X[1])

    def test_subclass_get_instance(self):
        X, Y, Z, W = self.cls[:4]

        self.assertEqual(X('a'), Y('a'))
        self.assertEqual(Y('b'), Z('b'))
        self.assertEqual(Z('c'), W('c'))

        self.assertRaises(RuntimeError, X, 'test')
        self.assertRaises(RuntimeError, W, 'test')
        self.assertRaises(RuntimeError, Y, 'invalid-name')
        self.assertRaises(RuntimeError, Z, 'invalid-name')

    def test_subclass_repeated(self):
        X = self.cls[0]

        # Cannot repeat key from parent
        self. assertRaises(RuntimeError, type, 'SubX', (X,),
                           {'_keys': ['a', 'z']})

        # Cannot repeat key from this same class
        self. assertRaises(RuntimeError, type, 'SubX', (X,),
                           {'_keys': ['z', 'z']})

    def test_method(self):
        X, Y, Z = self.cls[:3]

        if v3:
            # Methods bound to classes will not work (old Py2k behavior)
            self.assertEqual(Z.f(Z.a), Z.a.value + 1)
            self.assertEqual(Z.f(Z.b), Z.b.value + 1)

        self.assertEqual(Z.c.f(), Z.c.value + 1)


class ObjTestMultipleSubclass(unittest.TestCase):

    def setUp(self):
        class A(o.Obj):
            a, b = 1, 2

        class B(o.Obj):
            c, d = 3, 4

        class C(o.Obj):
            c, d = 3, 2

        class D(o.Obj):
            b, c = 3, 4

        self.cls = A, B, C, D

    def test_multiple_subclass(self):
        A, B, C, D = self.cls

        # Py2.x do not accept `metaclass=no_conflict` syntax
        E = o.no_conflict('E', (A, B), {})
        F = o.no_conflict('F', (A, B), {'e': 5})

        self.assertEqual(F.a.value, 1)
        self.assertEqual(E.b.value, 2)
        self.assertEqual(F.c.value, 3)
        self.assertEqual(E.d.value, 4)
        self.assertEqual(F.e.value, 5)

    def test_multiple_subclass_clash(self):
        A, B, C, D = self.cls
        # Key clash
        self.assertRaises(TypeError, o.no_conflict, 'X', A, C, {})
        self.assertRaises(TypeError, o.no_conflict, 'X', C, A, {})

        # Name clash
        self.assertRaises(TypeError, o.no_conflict, 'X', A, D, {})
        self.assertRaises(TypeError, o.no_conflict, 'X', D, A, {})

        # Both
        self.assertRaises(TypeError, o.no_conflict, 'X', C, D, {})
        self.assertRaises(TypeError, o.no_conflict, 'X', D, C, {})


class Lookup_Possible(o.Obj):
    a, b = keys(2)


class OtherTests(unittest.TestCase):

    def test_pickle(self):
        import pickle

        X = Lookup_Possible

        _X = pickle.loads(pickle.dumps(X))
        _X_a = pickle.loads(pickle.dumps(X.a))
        _X_b = pickle.loads(pickle.dumps(X.b))

        self.assertEqual(X, _X)
        self.assertEqual(X.a, _X_a)
        self.assert_(X.b is _X_b)

    def test_isinstance(self):

        class C(o.Obj):
            a, b = 1, 2

        class D(C):
            c, d = keys(2)

        self.assert_(isinstance(C.a, D))
        self.assert_(isinstance(C.b, D))
        self.assert_(isinstance(D.a, C))
        self.assert_(isinstance(D.b, C))
        self.assert_(isinstance(D.c, C))
        self.assert_(isinstance(D.d, C))
