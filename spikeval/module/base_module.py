# -*- coding: utf-8 -*-
#
# spikeval - module.base_module.py
#
# Philipp Meier <pmeier82 at googlemail dot com>
# 2011-09-29
#

"""module class object for implementing  sorting metrics for evaluation"""
__author__ = 'Philipp Meier <pmeier82 at googlemail dot com>'
__docformat__ = 'restructuredtext'



##---IMPORTS



##---class

class BaseModule(object):
    """base class for evaluation modules

    An evaluation module is a self-contained evaluation step,
    like the application of a single metric or the generation of plots.

    All modules must implement this interface work in the evaluation
    framework!
    """

    def __init__(self):
        """
        :return:
        """

##---MAIN

if __name__ == '__main__':
    pass
