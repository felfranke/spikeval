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

import unittest


##---TESTS

class TestImports(unittest.TestCase):
    """test case for package imports"""

    def test_scipy(self):
        """test for scipy"""

        import scipy

        self.assertGreaterEqual(scipy.__version__, '0.7.0')

    def test_tables(self):
        """test for tables"""

        import tables

        self.assertGreaterEqual(tables.__version__, '2.1.2')

    def test_matplotlib(self):
        """test for matplotlib"""

        import matplotlib

        self.assertGreaterEqual(matplotlib.__version__, '0.99.3')
        self.assertEqual(matplotlib.validate_backend('agg'), 'agg')


if __name__ == '__main__':
    unittest.main()
