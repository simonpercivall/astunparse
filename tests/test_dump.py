import ast
import re
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import astunparse
from tests.common import AstunparseCommonTestCase

class DumpTestCase(AstunparseCommonTestCase, unittest.TestCase):

    def assertASTEqual(self, dump1, dump2):
        # undo the pretty-printing
        dump1 = re.sub(r"(?<=[\(\[])\n\s+", "", dump1)
        dump1 = re.sub(r"\n\s+", " ", dump1)
        self.assertEqual(dump1, dump2)

    def check_roundtrip(self, code1, filename="internal", mode="exec"):
        ast_ = compile(str(code1), filename, mode, ast.PyCF_ONLY_AST)
        dump1 = astunparse.dump(ast_)
        dump2 = ast.dump(ast_)
        self.assertASTEqual(dump1, dump2)
