# -*- coding: utf-8 -*-
#
# spikeval - core.py
#
# Philipp Meier - <pmeier82 at gmail dot com>
# 2011-10-10
#

"""spike sorting evaluation website - alignment using tha old 'align spike
trains' routine from SpikePy"""
__docformat__ = 'restructuredtext'


##---IMPORTS

import sys
import scipy as sp
from .logging import Logger
from .module.alignment_old import align_spike_trains as eval_metric
from .module.general_plots import do_plotting


##---FUNCTIONS

def eval_core(raw_data, sts_gt, sts_ev, metric_cls, log=sys.stdout):
    """core function to produce one evaluation result based on one set of
    data, ground truth spike train and estimated spike train.

    :type raw_data: ndarray
    :param raw_data: raw data as ndarray with [samples, channels]
    :type sts_gt: dict
    :param sts_gt: ground truth spike train set
    :type sts_ev: dict
    :param sts_ev: evaluation spike train set
    :type module: EvalMetric
    :param module: evaluation module to apply to the inputs
    :type log: file-like
    :param log: stream to log to
        Default=sys.stdout
    :returns: EvalMetric instance or None on error inputs if module could be
        applied to the inputs, False else
    """

    ## inits and checks
    metric = None
    logger = Logger(log)

    # start module
    try:
        metric = metric_cls(raw_data, sts_gt, sts_ev, logger)
    except Exception, ex:
        logger.log_delimiter_line()
        logger.log(str(ex))
        logger.log_delimiter_line()
    finally:
        return metric

##--- MAIN
if __name__ == '__main__':
    sorting_eval(r'/www/eval/application/python',
                 r'021_C_Easy1_noise01.gdf',
                 r'/www/eval/groundtruth',
                 r'C_Easy1_noise005_groundtruth.mat',
                 r'/www/eval/application/python/results')
