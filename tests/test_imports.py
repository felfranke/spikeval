# -*- coding: utf-8 -*-
#
# tests - test_imports.py
#
# Philipp Meier - <pmeier82 at gmail dot com>
# 2011-10-11
#

"""unit tests for packages and environment"""
__docformat__ = 'restructuredtext'


##---IMPORTS

try:
    # for python < 2.7.x
    import unittest2 as unittest
except ImportError:
    import unittest


##---TESTS

class TestImports(unittest.TestCase):
    """test case for package imports"""

    def test_scipy(self):
        """test for scipy"""

        import scipy

        self.assertGreaterEqual(scipy.__version__, '0.6')

    def test_tables(self):
        """test for tables"""

        import tables

        self.assertGreaterEqual(tables.__version__, '2.0')

    def test_matplotlib(self):
        """test for matplotlib"""

        import matplotlib

        self.assertGreaterEqual(matplotlib.__version__, '0.98')
        self.assertEqual(matplotlib.validate_backend('agg'), 'agg')

    def test_texttable(self):
        """test for texttable"""

        import texttable

        self.assertGreaterEqual(texttable.__version__, '0.8')

    def test_pil_image(self):
        """test for PIL Image"""

        import Image

        self.assertGreaterEqual(Image.VERSION, '1.1.6')

    def test_mdp(self):
        """test for modular toolkit for data processing"""

        import mdp

        self.assertGreaterEqual(mdp.__version__, '2.5')

if __name__ == '__main__':
    unittest.main()
