import re
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import astunparse
from tests.common import ASTTestCase, AST3TestCase, AST2TestCase

class DumpTestCase(object):

    def assertASTEqual(self, dump1, dump2):
        # undo the pretty-printing
        dump1 = re.sub(r"(?<=[\(\[])\n\s+", "", dump1)
        dump1 = re.sub(r"\n\s+", " ", dump1)
        self.assertEqual(dump1, dump2)

    def check_roundtrip(self, code1, filename="internal", mode="exec"):
        ast_ = self.compile(str(code1), filename, mode)
        dump1 = astunparse.dump(ast_)
        dump2 = self.ast.dump(ast_)
        self.assertASTEqual(dump1, dump2)


class ASTDumpTestCase(DumpTestCase, ASTTestCase, unittest.TestCase):
    pass


if AST3TestCase:
    class AST3DumpTestCase(DumpTestCase, AST3TestCase, unittest.TestCase):
        pass


if AST2TestCase:
    class AST3DumpTestCase(DumpTestCase, AST2TestCase, unittest.TestCase):
        pass
