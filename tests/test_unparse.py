import ast
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import astunparse
from tests.common import ASTTestCase, AST3TestCase, AST2TestCase

class UnparseTestCase(object):

    def assertASTEqual(self, ast1, ast2):
        self.assertEqual(ast.dump(ast1), ast.dump(ast2))

    def check_roundtrip(self, code1, filename="internal", mode="exec"):
        ast1 = self.compile(str(code1), filename, mode)
        code2 = astunparse.unparse(ast1)
        ast2 = self.compile(code2, filename, mode)
        self.assertASTEqual(ast1, ast2)


class ASTUnparseTestCase(UnparseTestCase, ASTTestCase, unittest.TestCase):
    pass


if AST3TestCase:
    class AST3UnparseTestCase(UnparseTestCase, AST3TestCase, unittest.TestCase):
        pass


if AST2TestCase:
    class AST3UnparseTestCase(UnparseTestCase, AST2TestCase, unittest.TestCase):
        pass
