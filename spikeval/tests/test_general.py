# -*- coding: utf-8 -*-
#
# spikeval - tests/test_general.py
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

        good = True
        try:
            import scipy
        except:
            good = False
        self.assertEqual(good, True)


if __name__ == '__main__':
    unittest.main()
