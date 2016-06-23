import os
import re
import ast
import sys
import astunparse
from tests.test_unparse import UnparseTestCase, read_pyfile


class DumpTestCase(UnparseTestCase):
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


class DirectoryTestCase(DumpTestCase):
    """Test dump behaviour on all files in Lib and Lib/test."""
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

