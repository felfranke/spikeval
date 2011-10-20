# -*- coding: utf-8 -*-
#
# spikeval - module.base_module.py
#
# Philipp Meier <pmeier82 at googlemail dot com>
# 2011-09-29
#

"""module base class for implementing evaluation modules"""
__docformat__ = 'restructuredtext'
__all__ = ['BaseModule']



##---IMPORTS

import scipy as sp
from ..logging import Logger


##---class

class ModuleInputError(ValueError):
    pass


class ModuleExecutionError(RuntimeError):
    pass


class BaseModule(object):
    """base class for evaluation modules

    An evaluation module is a self-contained evaluation step,
    like the application of a single metric or the generation of plots.

    All modules must implement this interface to work in the evaluation
    framework! To implement a new module subclass BaseModule and implement
    all :self._check_*: methods.

    :self._check_raw_data: validates the raw data, and should raise an
        ModuleInputError if the raw data does not validate
    :self._check_sts: validates a spike train set, and should raise an
        ModuleInputError if the raw data does not validate
    :self._check_parameters; checks the optional parameters and should
        return a dict containing all optional parameters initialised to
        their default values or set to the passed values.
    :self.apply: is the execution content of the module and should implement
        the module and store any results in :self.result:.

    You may log any useful information using :self.logger:,
    which is a :Logger: instance.
    """

    RESULT_TYPES = []

    def __init__(self, raw_data, sts_gt, sts_ev, log, **params):
        """
        :type raw_data: ndarray or None
        :param raw_data: raw data as ndarray with [samples, channels]
        :type sts_gt: dict
        :param sts_gt: ground truth spike train set
        :type sts_ev: dict
        :param sts_ev: evaluation spike train set
        :type log: Logger or file-like
        :param log: stream to log to
        """

        # inits and checks
        self.logger = Logger.get_logger(log)
        self.check_raw_data(raw_data)
        self.check_sts(sts_gt)
        self.check_sts(sts_ev)
        self.raw_data = raw_data
        self.sts_gt = sts_gt
        self.sts_ev = sts_ev
        self.params = params
        self.result = []

    def check_raw_data(self, raw_data):
        """check if :raw_data: is valid raw data

        :type raw_data: ndarray
        :param raw_data: raw data
        :raise ModuleInputError: if :raw_data: does not validate
        """

        self._check_raw_data(raw_data)

    def _check_raw_data(self, raw_data):
        raise NotImplementedError

    def check_sts(self, sts):
        """check if :sts: is a valid spike train set

        :type sts: dict
        :param sts: spike train set to validate
        :raise ModuleInputError: if :sts: does not validate
        """

        self._check_sts(sts)

    def _check_sts(self, sts):
        raise NotImplementedError

    def check_parameters(self, parameters):
        """check parameters

        :type parameters
        :param parameters:
        :return: valid parameters
        """

        return self._check_paramters(parameters)

    def _check_parameters(self):
        raise NotImplementedError

    def apply(self):
        pass

##---MAIN

if __name__ == '__main__':
    pass
