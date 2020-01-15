import codecs
import os
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import six
if six.PY3:
    import tokenize
else:
    from lib2to3.pgen2 import tokenize

def read_pyfile(filename):
    """Read and return the contents of a Python source file (as a
    string), taking into account the file encoding."""
    if six.PY3:
        with open(filename, "rb") as pyfile:
            encoding = tokenize.detect_encoding(pyfile.readline)[0]
        with codecs.open(filename, "r", encoding=encoding) as pyfile:
            source = pyfile.read()
    else:
        with open(filename, "r") as pyfile:
            source = pyfile.read()
    return source

code_parseable_in_all_parser_modes = """\
(a + b + c) * (d + e + f)
"""

for_else = """\
def f():
    for x in range(10):
        break
    else:
        y = 2
    z = 3
"""

while_else = """\
def g():
    while True:
        break
    else:
        y = 2
    z = 3
"""

relative_import = """\
from . import fred
from .. import barney
from .australia import shrimp as prawns
"""

import_many = """\
import fred, barney
"""

nonlocal_ex = """\
def f():
    x = 1
    def g():
        nonlocal x
        x = 2
        y = 7
        def h():
            nonlocal x, y
"""

# also acts as test for 'except ... as ...'
raise_from = """\
try:
    1 / 0
except ZeroDivisionError as e:
    raise ArithmeticError from e
"""

async_comprehensions_and_generators = """\
async def async_function():
    my_set = {i async for i in aiter() if i % 2}
    my_list = [i async for i in aiter() if i % 2]
    my_dict = {i: -i async for i in aiter() if i % 2}
    my_gen = (i ** 2 async for i in agen())
    my_other_gen = (i - 1 async for i in agen() if i % 2)
"""

class_decorator = """\
@f1(arg)
@f2
class Foo: pass
"""

elif1 = """\
if cond1:
    suite1
elif cond2:
    suite2
else:
    suite3
"""

elif2 = """\
if cond1:
    suite1
elif cond2:
    suite2
"""

try_except_finally = """\
try:
    suite1
except ex1:
    suite2
except ex2:
    suite3
else:
    suite4
finally:
    suite5
"""

with_simple = """\
with f():
    suite1
"""

with_as = """\
with f() as x:
    suite1
"""

with_two_items = """\
with f() as x, g() as y:
    suite1
"""

a_repr = """\
`{}`
"""

complex_f_string = '''\
f\'\'\'-{f"""*{f"+{f'.{x}.'}+"}*"""}-\'\'\'
'''

async_function_def = """\
async def f():
    suite1
"""

async_for = """\
async def f():
    async for _ in reader:
        suite1
"""

async_with = """\
async def f():
    async with g():
        suite1
"""

async_with_as = """\
async def f():
    async with g() as x:
        suite1
"""

class AstunparseCommonTestCase:
    # Tests for specific bugs found in earlier versions of unparse

    def assertASTEqual(self, dump1, dump2):
        raise NotImplementedError()

    def check_roundtrip(self, code1, filename="internal", mode="exec"):
        raise NotImplementedError()

    test_directories = [
        os.path.join(getattr(sys, 'real_prefix', sys.prefix),
                     'lib', 'python%s.%s' % sys.version_info[:2])]

    def test_files(self):
        names = []
        for test_dir in self.test_directories:
            for n in os.listdir(test_dir):
                if n.endswith('.py') and not n.startswith('bad'):
                    names.append(os.path.join(test_dir, n))

        for filename in names:
            print('Testing %s' % filename)
            source = read_pyfile(filename)
            self.check_roundtrip(source)

    def test_parser_modes(self):
        for mode in ['exec', 'single', 'eval']:
            self.check_roundtrip(code_parseable_in_all_parser_modes, mode=mode)

    def test_del_statement(self):
        self.check_roundtrip("del x, y, z")

    def test_shifts(self):
        self.check_roundtrip("45 << 2")
        self.check_roundtrip("13 >> 7")

    def test_for_else(self):
        self.check_roundtrip(for_else)

    def test_while_else(self):
        self.check_roundtrip(while_else)

    def test_unary_parens(self):
        self.check_roundtrip("(-1)**7")
        self.check_roundtrip("(-1.)**8")
        self.check_roundtrip("(-1j)**6")
        self.check_roundtrip("not True or False")
        self.check_roundtrip("True or not False")

    @unittest.skipUnless(sys.version_info < (3, 6), "Only works for Python < 3.6")
    def test_integer_parens(self):
        self.check_roundtrip("3 .__abs__()")

    def test_huge_float(self):
        self.check_roundtrip("1e1000")
        self.check_roundtrip("-1e1000")
        self.check_roundtrip("1e1000j")
        self.check_roundtrip("-1e1000j")

    @unittest.skipUnless(six.PY2, "Only works for Python 2")
    def test_min_int27(self):
        self.check_roundtrip(str(-sys.maxint-1))
        self.check_roundtrip("-(%s)" % (sys.maxint + 1))

    @unittest.skipUnless(six.PY3, "Only works for Python 3")
    def test_min_int30(self):
        self.check_roundtrip(str(-2**31))
        self.check_roundtrip(str(-2**63))

    def test_imaginary_literals(self):
        self.check_roundtrip("7j")
        self.check_roundtrip("-7j")
        self.check_roundtrip("0j")
        self.check_roundtrip("-0j")
        if six.PY2:
            self.check_roundtrip("-(7j)")
            self.check_roundtrip("-(0j)")

    def test_negative_zero(self):
        self.check_roundtrip("-0")
        self.check_roundtrip("-(0)")
        self.check_roundtrip("-0b0")
        self.check_roundtrip("-(0b0)")
        self.check_roundtrip("-0o0")
        self.check_roundtrip("-(0o0)")
        self.check_roundtrip("-0x0")
        self.check_roundtrip("-(0x0)")

    def test_lambda_parentheses(self):
        self.check_roundtrip("(lambda: int)()")

    def test_chained_comparisons(self):
        self.check_roundtrip("1 < 4 <= 5")
        self.check_roundtrip("a is b is c is not d")

    def test_function_arguments(self):
        self.check_roundtrip("def f(): pass")
        self.check_roundtrip("def f(a): pass")
        self.check_roundtrip("def f(b = 2): pass")
        self.check_roundtrip("def f(a, b): pass")
        self.check_roundtrip("def f(a, b = 2): pass")
        self.check_roundtrip("def f(a = 5, b = 2): pass")
        self.check_roundtrip("def f(*args, **kwargs): pass")
        if six.PY3:
            self.check_roundtrip("def f(*, a = 1, b = 2): pass")
            self.check_roundtrip("def f(*, a = 1, b): pass")
            self.check_roundtrip("def f(*, a, b = 2): pass")
            self.check_roundtrip("def f(a, b = None, *, c, **kwds): pass")
            self.check_roundtrip("def f(a=2, *args, c=5, d, **kwds): pass")

    def test_relative_import(self):
        self.check_roundtrip(relative_import)

    def test_import_many(self):
        self.check_roundtrip(import_many)

    @unittest.skipUnless(six.PY3, "Only for Python 3")
    def test_nonlocal(self):
        self.check_roundtrip(nonlocal_ex)

    @unittest.skipUnless(six.PY3, "Only for Python 3")
    def test_raise_from(self):
        self.check_roundtrip(raise_from)

    def test_bytes(self):
        self.check_roundtrip("b'123'")

    @unittest.skipIf(sys.version_info < (3, 6), "Not supported < 3.6")
    def test_formatted_value(self):
        self.check_roundtrip('f"{value}"')
        self.check_roundtrip('f"{value!s}"')
        self.check_roundtrip('f"{value:4}"')
        self.check_roundtrip('f"{value!s:4}"')

    @unittest.skipIf(sys.version_info < (3, 6), "Not supported < 3.6")
    def test_joined_str(self):
        self.check_roundtrip('f"{key}={value!s}"')
        self.check_roundtrip('f"{key}={value!r}"')
        self.check_roundtrip('f"{key}={value!a}"')

    @unittest.skipIf(sys.version_info != (3, 6, 0), "Only supported on 3.6.0")
    def test_joined_str_361(self):
        self.check_roundtrip('f"{key:4}={value!s}"')
        self.check_roundtrip('f"{key:02}={value!r}"')
        self.check_roundtrip('f"{key:6}={value!a}"')
        self.check_roundtrip('f"{key:4}={value:#06x}"')
        self.check_roundtrip('f"{key:02}={value:#06x}"')
        self.check_roundtrip('f"{key:6}={value:#06x}"')
        self.check_roundtrip('f"{key:4}={value!s:#06x}"')
        self.check_roundtrip('f"{key:4}={value!r:#06x}"')
        self.check_roundtrip('f"{key:4}={value!a:#06x}"')

    @unittest.skipUnless(six.PY2, "Only for Python 2")
    def test_repr(self):
        self.check_roundtrip(a_repr)

    @unittest.skipUnless(sys.version_info[:2] >= (3, 6), "Only for Python 3.6 or greater")
    def test_complex_f_string(self):
        self.check_roundtrip(complex_f_string)

    @unittest.skipUnless(six.PY3, "Only for Python 3")
    def test_annotations(self):
        self.check_roundtrip("def f(a : int): pass")
        self.check_roundtrip("def f(a: int = 5): pass")
        self.check_roundtrip("def f(*args: [int]): pass")
        self.check_roundtrip("def f(**kwargs: dict): pass")
        self.check_roundtrip("def f() -> None: pass")

    @unittest.skipIf(sys.version_info < (2, 7), "Not supported < 2.7")
    def test_set_literal(self):
        self.check_roundtrip("{'a', 'b', 'c'}")

    @unittest.skipIf(sys.version_info < (2, 7), "Not supported < 2.7")
    def test_set_comprehension(self):
        self.check_roundtrip("{x for x in range(5)}")

    @unittest.skipIf(sys.version_info < (2, 7), "Not supported < 2.7")
    def test_dict_comprehension(self):
        self.check_roundtrip("{x: x*x for x in range(10)}")

    @unittest.skipIf(sys.version_info < (3, 6), "Not supported < 3.6")
    def test_dict_with_unpacking(self):
        self.check_roundtrip("{**x}")
        self.check_roundtrip("{a: b, **x}")

    @unittest.skipIf(sys.version_info < (3, 6), "Not supported < 3.6")
    def test_async_comp_and_gen_in_async_function(self):
        self.check_roundtrip(async_comprehensions_and_generators)

    @unittest.skipIf(sys.version_info < (3, 7), "Not supported < 3.7")
    def test_async_comprehension(self):
        self.check_roundtrip("{i async for i in aiter() if i % 2}")
        self.check_roundtrip("[i async for i in aiter() if i % 2]")
        self.check_roundtrip("{i: -i async for i in aiter() if i % 2}")

    @unittest.skipIf(sys.version_info < (3, 7), "Not supported < 3.7")
    def test_async_generator_expression(self):
        self.check_roundtrip("(i ** 2 async for i in agen())")
        self.check_roundtrip("(i - 1 async for i in agen() if i % 2)")

    def test_class_decorators(self):
        self.check_roundtrip(class_decorator)

    @unittest.skipUnless(six.PY3, "Only for Python 3")
    def test_class_definition(self):
        self.check_roundtrip("class A(metaclass=type, *[], **{}): pass")

    def test_elifs(self):
        self.check_roundtrip(elif1)
        self.check_roundtrip(elif2)

    def test_try_except_finally(self):
        self.check_roundtrip(try_except_finally)

    @unittest.skipUnless(six.PY3, "Only for Python 3")
    def test_starred_assignment(self):
        self.check_roundtrip("a, *b, c = seq")
        self.check_roundtrip("a, (*b, c) = seq")
        self.check_roundtrip("a, *b[0], c = seq")
        self.check_roundtrip("a, *(b, c) = seq")

    @unittest.skipIf(sys.version_info < (3, 6), "Not supported < 3.6")
    def test_variable_annotation(self):
        self.check_roundtrip("a: int")
        self.check_roundtrip("a: int = 0")
        self.check_roundtrip("a: int = None")
        self.check_roundtrip("some_list: List[int]")
        self.check_roundtrip("some_list: List[int] = []")
        self.check_roundtrip("t: Tuple[int, ...] = (1, 2, 3)")
        self.check_roundtrip("(a): int")
        self.check_roundtrip("(a): int = 0")
        self.check_roundtrip("(a): int = None")

    def test_with_simple(self):
        self.check_roundtrip(with_simple)

    def test_with_as(self):
        self.check_roundtrip(with_as)

    @unittest.skipIf(sys.version_info < (2, 7), "Not supported < 2.7")
    def test_with_two_items(self):
        self.check_roundtrip(with_two_items)

    @unittest.skipIf(sys.version_info < (3, 5), "Not supported < 3.5")
    def test_async_function_def(self):
        self.check_roundtrip(async_function_def)

    @unittest.skipIf(sys.version_info < (3, 5), "Not supported < 3.5")
    def test_async_for(self):
        self.check_roundtrip(async_for)

    @unittest.skipIf(sys.version_info < (3, 5), "Not supported < 3.5")
    def test_async_with(self):
        self.check_roundtrip(async_with)

    @unittest.skipIf(sys.version_info < (3, 5), "Not supported < 3.5")
    def test_async_with_as(self):
        self.check_roundtrip(async_with_as)
