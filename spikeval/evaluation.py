# -*- coding: utf-8 -*-
#
# spikeval - evaluation_base.py
#
# Philipp Meier - <pmeier82 at gmail dot com>
# 2011-08-16
#

"""spike sorting evaluation website - evaluation pipeline"""
__docformat__ = 'restructuredtext'


##---IMPORTS

from multiprocessing import Process


##---CLASSES

class EvalException(Exception):
    pass

class PersistantObjectHandle(object):
    pass

class ModuleInput(PersistantObjectHandle):
    """module input object"""

    ## constructor

    def __init__(self):
        """
        :Parameters:
            url : str
                str to the path where the benchmark can be loaded from
        """

        super(ModuleInput, self).__init__()
        self._data = None

    def load(self, load_path): ## TODO: implement
        """abstract load method"""

        raise NotImplementedError


## result classes

class ModuleOutput(PersistantObjectHandle):
    """module output object"""


class Figure(ModuleOutput):
    """figure output"""


class Table(ModuleOutput):
    """table output"""


class Dict(dict, ModuleOutput):
    """dict output"""


## module class

class Module(Process):
    """single step module for the spikesorting evaluation website"""

    ## class variables

    USE_GROUNDTRUTH = None
    USE_RAW_DATA = None
    USE_SPIKES = None

    ## constructor

    def __init__(self, benchmark, upload, results_dir):
        """
        :Parameters:
            benchmark : Benchmark
            upload : Upload
            results_dir : str
                path to an existing directory where results will be put
        """

        super(Module, self).__init__()

        if not isinstance(benchmark, ModuleInput):
            raise TypeError('expected Benchmark object, got %s' %
                            benchmark.__class__)
        self.benchmark = benchmark
        if not isinstance(upload, ModuleInput):
            raise TypeError('expected Upload object, got %s' %
                            upload.__class__)
        self.upload = upload
        self.results = []
        self.check_input(self.benchmark, self.upload)

    ## interface

    def process(self):
        """calls the module content"""

        raise NotImplementedError

    def run(self):
        """detaches the process to the background before starting the module"""

        self.process()

    ## internals

    @classmethod
    def check_input(cls, bm, ul):
        """checks whether this module is compatible with the benchmark and
        upload

        returns True if this module
        """

        # benchmark requirements
        if cls.USE_GROUNDTRUTH:
            if not bm.HAS_GROUNDTRUTH:
                raise EvalException('benchmark misses groundtruth!')
        if cls.USE_RAW_DATA:
            if not bm.HAS_RAW_DATA:
                raise EvalException('benchmark misses raw data!')
        if cls.USE_SPIKES:
            if not bm.USE_SPIKES:
                raise EvalException('benchmark misses raw spikes!')


##---MAIN

if __name__ == '__main__':
    pass
