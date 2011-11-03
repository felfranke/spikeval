# -*- coding: utf-8 -*-
#
# tests - test_django_entry_point.py
#
# Philipp Meier - <pmeier82 at gmail dot com>
# 2011-11-01
#

"""unit tests for django entry point"""
__docformat__ = 'restructuredtext'


##---IMPORTS

try:
    # for python < 2.7.x
    import unittest2 as unittest
except ImportError:
    import unittest


##---TESTS

class TestLogging(unittest.TestCase):
    """test case for logging"""

    def setUp(self):
        self.str_test = ['test1', 'test2', 'test3']

    def test_xxx(self):
        pass

if __name__ == '__main__':
    unittest.main()
