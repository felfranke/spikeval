# -*- coding: utf-8 -*-
#
# spikeval - django_entry_point.py
#
# Philipp Meier - <pmeier82 at gmail dot com>
# 2011-10-14
#

"""django specific functions and entry point"""
__docformat__ = 'restructuredtext'
__all__ = ['check_record', 'start_eval']


##---IMPORTS

import sys
from .core import eval_core
from .datafiles import read_gdf_sts, read_hdf5_arc
from .logging import Logger
from .module import MODULES


##---DUMMY CLASSES FOR DJANGO ORM
# i could not have the code run any tests as i dont know how to properly
# import the django model classes. so i implemented these dummies here,
# I hope all the relevant information is still in the dummies and my concept
# of the behavior is right. please comment on this or rewrite on your own
# and send me a patch of this file.

class FileThingy(object):
    path = '/dev/null'


class DjangoORMField(object):
    def __init__(self, type=''):
        self.type = ''


class Record(object):
    """dummy for the benchmark file record"""

    def __init__(self, id=0):
        self.id = id
        self.verified = False
        self.verified_error = ''

        self.groundtruth = FileThingy()
        self.rawdatafile = FileThingy()

    def save(self):
        pass


class EvaluationResultsImg(object):
    """dummy for the evaluation results of pictures"""

    evaluation = DjangoORMField('eval_fk')
    gt_unit = DjangoORMField('str')
    found_unit = DjangoORMField('str')
    img_data = DjangoORMField('image')
    img_type = DjangoORMField('str') # or mapping

    def __init__(self, id=0):
        self.id = id
        self.error = False
        self.error_log = ''

    def save(self):
        pass


class EvaluationResultsStats(object):
    """dummy for the evaluation results of statics"""

    evaluation = DjangoORMField('eval_fk')
    date_created = DjangoORMField('date')

    gt_unit = DjangoORMField('str') #0
    found_unit = DjangoORMField('str') #1

    KS = DjangoORMField('int') #2
    KSO = DjangoORMField('int') #3
    FS = DjangoORMField('int') #4

    TP = DjangoORMField('int') #5
    TPO = DjangoORMField('int') #6

    FPA = DjangoORMField('int') #7
    FPAE = DjangoORMField('int') #8
    FPAO = DjangoORMField('int') #9
    FPAOE = DjangoORMField('int') #10

    FN = DjangoORMField('int') #11
    FNO = DjangoORMField('int') #12

    FP = DjangoORMField('int') #13

    def __init__(self, id=0):
        self.id = id
        self.error = False
        self.error_log = ''

    def save(self):
        pass

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
    :type log: file_like
    :param log: logging stream
        Default=sys.stdout

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
        gt = read_gdf_sts(gt_file_path)
        logger.log('found gt_file: %s' % gt_file_path)
        for st in gt:
            assert isinstance(st, sp.ndarray)
            assert st.ndim == 1
        logger.log('gt_file passed all checks')
        # TODO: more checks?

        # checking raw data file -- should be hdf5
        rd = read_hdf5_arc(rd_file_path)
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
def start_eval(path_rd, path_ev, path_gt, key, log=sys.stdout, **kwargs):
    """core function to produce one evaluation result based on one set of
    data, ground truth spike train and estimated spike train.

    :type path_rd: str
    :param path_rd: path to the file holding the raw data
    :type path_ev: str
    :param path_ev: path to the file holding the estimated spike train
    :type path_gt: str
    :param path_gt: path to the file holding the ground truth spike train
    :type key: int
    :param key: unique evaluation key
    :type log: file_like
    :param log: logging stream
        Default=sys.stdout
    :keyword ??: any, will be passed to modules as parameters

    :returns: None
    """

    # inits
    logger = Logger.get_logger(log)

    # read in evaluation file
    logger.log('reading input files')
    rd, sampling_rate = read_hdf5_arc(path_rd)
    if sampling_rate is not None:
        kwargs.update(sampling_rate=sampling_rate)
    ev = read_gdf_sts(path_ev)
    gt = read_gdf_sts(path_gt)
    logger.log('done reading input files')

    # apply modules
    logger.log('starting evaluation loop:')
    modules = []
    for mod_cls in MODULES:
        try:
            logger.log('starting module: %s' % mod_cls.__name__)
            this_mod = eval_core(rd, gt, ev, mod_cls, logger, **kwargs)
        except Exception, ex:
            logger.log_delimiter_line()
            logger.log(str(ex))
            logger.log_delimiter_line()
        finally:
            modules.append(this_mod)
    logger.log('done evaluating')

    logger.log('starting to save evaluation results')
    # care for static result mapping of images,
    # we will send PIL Image instances here!
    for i, t in enumerate(['wf_single', 'wf_all', 'clus12', 'clus34',
                           'clus_proj', 'spiketrain']):
        rval = EvaluationResultsImg(id=key)
        rval.img_data = modules[0][i].value
        rval.img_type = t
        rval.save()

    # care for static result mapping of alignment statistic,
    # we will send a MRTable instance here
    for row in modules[1][0].value:
        rval = EvaluationResultsStats(id=key)

        rval.gt_unit = row[0]
        rval.found_unit = row[1]

        rval.KS = row[2]
        rval.KSO = row[3]
        rval.FS = row[4]

        rval.TP = row[5]
        rval.TPO = row[6]

        rval.FPA = row[7]
        rval.FPAE = row[8]
        rval.FPAO = row[9]
        rval.FPAOE = row[10]

        rval.FN = row[11]
        rval.FNO = row[12]

        rval.FP = row[13]

        rval.save()
    logger.log('done saving results')

#    return modules

##---MAIN

if __name__ == '__main__':
    pass
