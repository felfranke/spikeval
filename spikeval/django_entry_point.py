# -*- coding: utf-8 -*-
#
# spikeval - django_entry_point.py
#
# Philipp Meier - <pmeier82 at gmail dot com>
# 2011-10-14
#

"""django specific functions and entry point"""
__docformat__ = 'restructuredtext'
__all__ = []


##---IMPORTS

import sys
from .core import eval_core
from .datafiles import read_gdf, read_hdf5
from .somewhere import Record, EvaluationResults
from .logging import Logger
from .module import MODULES


##---FUNCTIONS

#+Interface 1: The user uploads a file pair. The frontend calls a
#backend function with the following inputs:
#int Key - identifier for the benchmark upload
#
#the backend will use the key to instantiate an object with which it
#can access the uploaded files. The files will be opened and checked
#for the content and return a boolean if the check was successful and a
#string containing information about the check like errors.
#
#This check function could look like:
#
#function checkBenchmark(key)
#import Record
#record = Record.get(id = key)
#
#gtfilepath = record.groundtruth.path
#rawfilepath = record.raw_data.path
#
#[then check the files ... (gtfilepath, rawfilepath)]
#
#record.verfied = boolean
#recrod.verified_error = "string"
#
#return
def check_record(key, log=sys.stdout):
    """checks consistency of (raw_data, ground truth spike train) tuple

    :type key: int
    :param key: unique record identifier
    :type log: func
    :param log: logging function func(level, text), the default prints to fd1
        Default=dummy_log

    :returns: bool -- True if benchmark files comply, False else. Errors will
        be written to the comment section of the orm layer object referenced
        by the key.
    """

    # inits
    logger = Logger.get_logger(log)
    logger.log('starting record check for key=%d' % key)
    rec = Record(id=key)
    # XXX: check calling syntax/names!!
    gt_file_path = rec.groundtruth.path
    gt = None
    logger.log('gt_file_path: %s' % gt_file_path)
    rd_file_path = rec.rawdatafile.path
    rd = None
    logger.log('rd_file_path: %s' % rd_file_path)

    try:
        # checking ground truth spike train file -- should be gdf
        gt = read_gdf(gt_file_path)
        logger.log('found gt_file: %s' % gt_file_path)
        for st in gt:
            assert isinstance(st, sp.ndarray)
            assert st.ndim == 1
        logger.log('gt_file passed all checks')
        # TODO: more checks?

        # checking raw data file -- should be hdf5
        rd = read_hdf5(rd_file_path)
        logger.log('found rd_file: %s' % rd_file_path)
        assert 'sampling_rate' in rd
        srate = rd['sampling_rate']
        assert srate.ndim == 0
        assert 'data' in rd
        raw_data = rd['data']

        # TODO: more checks?

        rec.verified = True
    except Exception, ex:
        rec.verified = False
        rec.verified_error = str(ex)
        logger.log('error during record check: %s' % str(ex))

    # all checks passed
    rec.save()
    logger.log('passed record check for key=%d' % key)
    return rec.verfied

#+Interface 2: The user uploads a sorting result. The frontend calls a
#backend function and displays the state of the evaluation to the user.
#the backend instantiates an object with which to control that user
#output and return the log of the evaluation. This object will also
#store the evaluation results
#
#The function call gets the following inputs:
#1. path to upload file: str
#2. path to benchmark raw data file: str
#3. path to benchmark gt file: str
#4. key for this evaluation: int
#5. path to a temp directory: str
#
#The backend function does not return anything, all output will again
#be done by the Object e.g.
#import ResultsObject
#res = ResultsObject(id = key)
#
#res.log = "bla"
#res.image = Image
#...
def eval_core(path_rd, path_ev, path_gt, key, temp_dir='/tmp',
              log=sys.stdout, **kwargs):
    """core function to produce one evaluation result based on one set of
    data, ground truth spike train and estimated spike train.

    :type path_ev: str
    :param path_ev: path to the file holding the estimated spike train
    :type path_gt: str
    :param path_gt: path to the file holding the ground truth spike train
    :type path_rd: str
    :type path_rd: path to the file holding the raw data
    :type key: int
    :param key: unique evaluation key
    :type temp_dir: str
    :param temp_dir: path to a directory where temporary files may be stored
    :type log: func
    :param log: logging function func(level, text), the default prints to fd1
        Default=dummy_log
    :keyword ??: any, will be passed to modules

    :returns: None

    :raises: EvalError
    """

    # inits
    logger = Logger.get_logger(log)
    rval = EvaluationResults(id=Key)

    # read in evaluation file
    logger.log(1, '*-reading files')
    rd = read_hdf5(path_rd)
    ev = read_gdf(path_ev)
    gt = read_gdf(path_gt)
    logger.log('done reading files!')

    # apply modules
    logger.log('*-evaluation of data')
    modules = []
    for mod in MODULES:
        try:
            logger.log('starting module: %s' % mod.__name__)
            this_mod = mod(rd, gt, ev, logger, **kwargs)
            this_mod.apply()
        except Exception, ex:
            logger.log(str(ex))
        finally:
            modules.append(this_mod)
    logger.log('evaluation done!')

    # TODO: do something meaningful with the finalised modules (results)
    # XXX: unclear how to precede :(
    return modules

##---MAIN

if __name__ == '__main__':
    pass
