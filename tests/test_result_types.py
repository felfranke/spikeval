# -*- coding: utf-8 -*-
#
# tests - test_module.py
#
# Philipp Meier - <pmeier82 at gmail dot com>
# 2011-10-11
#

"""unit tests for packages and environment"""
__docformat__ = 'restructuredtext'


##---IMPORTS

try:
    import unittest
except ImportError:
    import unittest2 as unittest

import scipy as sp


##---TESTS

class TestBaseModule(unittest.TestCase):
    """test case for package imports"""

    def setUp(self):
        """setup input data"""

        self.raw_data = sp.randn(1000, 4)
        self.sts_gt = {0:sp.array(range(100, 1000, 100)),
                       1:sp.array(range(20, 1000, 100)),
                       3:sp.array([222, 444, 666, 888])}
        shift = 20
        self.sts_ev = {0:sp.array(range(100, 1000, 100)) + shift,
                       1:sp.array(range(20, 1000, 100)) + shift,
                       3:sp.array([222, 444, 666, 888]) + shift}

    def test_module(self):
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
