# -*- coding: utf-8 -*-
#
# spikeval - somewhere/__init__.py
#
# Philipp Meier <pmeier82 at googlemail dot com>
# 2011-10-10
#

"""proxy package for django model imports"""
__docformat__ = 'restructuredtext'


##---IMPORTS

from models_bmark import Benchmark, Record
from models_dfile import FileSystemStorage, Datafile, Version
from models_eval import Evaluation, EvaluationResults
