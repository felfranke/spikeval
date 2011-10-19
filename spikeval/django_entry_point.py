# -*- coding: utf-8 -*-
#
# spikeval - evaluation_base.py
#
# Philipp Meier - <pmeier82 at gmail dot com>
# 2011-10-14
#

"""django specific functions and entry point"""
__docformat__ = 'restructuredtext'


##---IMPORTS

from core import eval_core
from datafiles import read_gdf, read_hdf5
from somewhere import Record, EvaluationResults


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
def check_record(key, log=dummy_log):
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
    log(1, 'starting record check for key=%d' % key)
    rec = Record(id=key)
    # XXX: check calling syntax/names!!
    gt_file_path = rec.groundtruth.path
    gt = None
    log(1, 'gt_file_path: %s' % gt_file_path)
    rd_file_path = rec.rawdatafile.path
    rd = None
    log(1, 'rd_file_path: %s' % rd_file_path)

    try:
        # checking ground truth spike train file -- should be gdf
        gt = read_gdf(gt_file_path)
        log(1, 'found gt_file: %s' % gt_file_path)
        for st in gt:
            assert isinstance(st, sp.ndarray)
            assert st.ndim == 1
        log(1, 'gt_file passed all checks')
        # TODO: more checks?

        # checking raw data file -- should be hdf5
        rd = read_hdf5(rd_file_path)
        log(1, 'found rd_file: %s' % rd_file_path)
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
        log(1, 'error during record check: %s' % str(ex))

    # all checks passed
    rec.save()
    log(1, 'passed record check for key=%d' % key)
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
def eval_core(path_ev, path_rd, path_gt, key, temp_dir='/tmp', log=dummy_log):
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

    :returns: None

    :raises: EvalError
    """

    # inits
    rval = EvaluationResults(id=Key)

    # read in evaluation file
    log(1, '*-reading files')
    ev = read_gdf(path_ev)
    log(1, 'evaluation file read!')
    bm = read_hdf5(path_rd)
    log(1, 'gtfile: %s' % gt_file)
    log(" benchmark: ")
    log(benchmark)
    bm_filename = osp.join(base_dir, benchmark)
    log('groundtruth file found: %s' % bm_filename)
    groundtruth = read_file(bm_filename)
    log('groundtruth file read!')

    # calculate alignment
    log('*-evaluation of data')
    results = align_spike_trains(
        groundtruth,
        train,
        max_shift=35
    )

    log('evaluation done!')

    # generate charts
    log('*-generating plots')

    do_plotting(
        result_dir,
        bm_filename,
        train,
        results['delta_shift'],
        ev_file.split('.')[0]
    )
    log('plots done!')

    rval = {'results':results, 'train':train, 'benchmark':benchmark}
    return rval


def dummy_log(level, text):
    """prototype for the logging handle

    :param level: logging level
    :param text: text to log
    :return: None
    """

    print text

##---MAIN

if __name__ == '__main__':
    pass
