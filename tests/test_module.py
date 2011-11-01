# -*- coding: utf-8 -*-
#
# tests - test_module.py
#
# Philipp Meier - <pmeier82 at gmail dot com>
# 2011-10-11
#

"""unit tests for modules"""
__docformat__ = 'restructuredtext'


##---IMPORTS

import sys
import unittest
import scipy as sp
from spikeval.module.base_module import *
from spikeval.module.result_types import *
from spikeval.module.mod_plot_data import ModDataPlot


##---CLASSES

class MyTestModule(BaseModule):
    """test module"""

    RESULT_TYPES = [MRScalar, MRTable, MRDict, MRPlot]

    def _check_raw_data(self, raw_data):
        pass

    def _check_sts(self, sts):
        pass

    def _check_parameters(self, parameters):
        return parameters

##---TESTS

class TestModule(unittest.TestCase):
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

    def test_general_plots(self):
        """test for scipy"""

        mod = ModDataPlot(
            self.raw_data,
            self.sts_gt,
            self.sts_ev,
            sys.stdout)
        mod.apply()
        mod.result[0].value.show()
        self.assertEqual(mod.status, 'finalised')

if __name__ == '__main__':
    unittest.main()
