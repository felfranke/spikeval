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
import os
from spikeval.datafiles import *
from spikeval.django_entry_point import *


##---TESTS

class TestDjangoEntryPoint(unittest.TestCase):
    """test case django_entry_point.py"""

    # XXX: not sure what to test exactly, have no means of testing anyways :(

    def test_start_eval(self):
        gt, sr = read_hdf5_arc(os.path.join('..', 'resource',
                                            'bmark_test.h5'))
        sts = read_gdf_sts(os.path.join('..', 'resource', 'bmark_test.gdf'))
        start_eval()

##---MAIN

if __name__ == '__main__':
    unittest.main()
