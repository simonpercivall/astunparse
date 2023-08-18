import ast
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import astunparse
from tests.common import AstunparseCommonTestCase

class UnparseTestCase(AstunparseCommonTestCase, unittest.TestCase):

    def assertASTEqual(self, ast1, ast2):
        self.assertEqual(ast.dump(ast1), ast.dump(ast2))

    def assertParenthesisEqual(self, expected_code, converted_code):
        converted_left_count = converted_code.count('(')
        expected_left_count = expected_code.count("(")

        converted_right_count = converted_code.count(')')
        expected_right_count  = expected_code.count(")")

        self.assertEqual(expected_left_count, converted_left_count, msg=f'Code: {converted_code} has {converted_left_count} left parenthesis, but expected {expected_left_count}')
        self.assertEqual(expected_right_count, converted_right_count, f'Code: {converted_code} has {converted_right_count} right parenthesis, but expected {expected_right_count}')

    def check_roundtrip(self, code1, filename="internal", mode="exec", validate_parentesis=True):
        ast1 = compile(str(code1), filename, mode, ast.PyCF_ONLY_AST)
        code2 = astunparse.unparse(ast1)
        ast2 = compile(code2, filename, mode, ast.PyCF_ONLY_AST)

        self.assertASTEqual(ast1, ast2)
        self.assertParenthesisEqual(code1, code2)
