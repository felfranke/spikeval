# -*- coding: utf-8 -*-
#
# spikeval - module.__init__.py
#
# Philipp Meier <pmeier82 at googlemail dot com>
# 2011-09-29
#

"""modules for evaluation"""
__docformat__ = 'restructuredtext'


##---IMPORTS

from .base_module import *
from .result_types import *
from .mod_default_visual import *
from .mod_metric_franke import *

##---MODULES

MODULES = [ModDefaultVisual, ModMetricFranke]
