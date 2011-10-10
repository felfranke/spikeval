# -*- coding: utf-8 -*-
#
# spikeval - evaljob.py
#
# Philipp Meier - <pmeier82 at gmail dot com>
# 2009-05-15
#
# $Id: evaluation.py 4796 2010-05-21 15:25:58Z ff $
#

"""evaluation job interface

change self.LOG.info:
version 0.1: was the old style.. never mention it again :)
version 0.2: load balancing and table in results
version 0.3: plots are pretty AND correct now :)
version 0.4: redesign without queues and terminating processes due to memory
             issues with long-running interpreter processes
version 0.5: redesign as callable script
version 0.6: redesign as callable script for use in G-Node django framwork
"""
__docformat__ = 'restructuredtext'
__version__ = '0.6'


#--- IMPORTS

# builtins
import os, os.path as osp
# packages
import MySQLdb
from scipy import ndarray
from multiprocessing import Process
from logging import getLogger
# spike
from datafiles import read_file
from sortingeval import sorting_eval


#--- CLASSES

class Evaluation(Process):
    """per file evaluation

    The evaluation works on data assumed to exist on locations in the local
    filesytem. That data is evaluated and results are save to back to the
    filesystem. Places where to look for data and where to save results to etc.
    are specified in the passed 'ConfigParser' object.
    """

    # constructor
    def __init__(self, key, ev_file, gt_file, log=None):
        """
        :Parameters:
            key : str
                The job identifier.
            cfg : ConfigParser
                Config file details. You should validate the config file outside
                befor calling the class. It is assumed its complete and valid.
            ev_file : path
                Path to the evaluation file. (.gdf)
            gt_file : path
                Path to the groundtruth file. (.mat)
        """

        # super
        super(Evaluation, self).__init__(name='Evaluation(%s)' % key)

        # init config
        self.log = log or getLogger()
        self.key = key
        self.ev_file = ev_file
        self.gt_file = gt_file
        self.basedir = self.cfg.get('DATADIRS', 'gt_dir')
        self.datadir = osp.join(self.cfg.get('DATADIRS', 'ul_dir'), self.key)
        self.rsltdir = osp.join(self.datadir, 'results')
        if not osp.exists(self.rsltdir):
            os.mkdir(self.rsltdir)
            self.adjust_perm(self.rsltdir)

    # process method
    def process(self):
        """run the evaluation in a detached process"""

        self.log.info('#-self.LOG.info FILE for file: %s/%s' % (self.key, self.ev_file))
        self.log.info('version: %s' % __version__)

        try:
            # lets skip potentially dangerous uri's
            if not osp.isfile(osp.join(self.datadir, self.ev_file)) or\
               osp.islink(osp.join(self.datadir, self.ev_file)) or\
               osp.ismount(osp.join(self.datadir, self.ev_file)):
                raise IOError('%s is not a proper file!' % self.ev_file)
            this = {'version': __version__}

            # call the evaluation
            ev = sorting_eval(self.datadir, self.ev_file,
                              self.basedir,
                              self.gt_file,
                              self.rsltdir, self.log.info)

            this['results'] = ev['results']
            this['train'] = ev['train']
            benchmark = ev['benchmark']

            # slim data
            del this['results']['alignment']
            self.log.info('evaluation done!')

            # data handling
            self.log.info('*-adjusting permissions')
            for f in os.listdir(self.rsltdir):
                self.adjust_perm(osp.join(self.rsltdir, f))
            self.log.info('adjusting permissions done!')

            # call hook
            self.log.info('*-calling hook')
            hook_scr = osp.basename(self.cfg.get('HOOK', 'hookscript'))
            hook_dir = osp.dirname(self.cfg.get('HOOK', 'hookscript'))
            if hook_dir is '':
                hook_dir = '.'
            if osp.exists(osp.join(hook_dir, hook_scr)):
                cmd = 'cd %s && php %s %s %s' % (
                    hook_dir,
                    hook_scr,
                    self.key,
                    self.ev_file
                    )
                self.log.info('command: %s' % cmd)
                rval = os.system(cmd)
                self.log.info('rval: %s' % rval)
            else:
                self.log.info('hook script not found: %s' % osp.join(hook_dir, hook_scr))

            # done!
            self.log.info('DONE FOR: %s/%s' % (self.key, self.ev_file))

        except Exception, ex:
            self.log.exception(ex)
            #        finally:
            #            return this

    def run(self):
        self.process()

    def adjust_perm(self, path):
        """set permissions acording to config file

        :Parameters:
            path : path
                The path to operate on.
        :Returns:
            True on success, False else.
        """

        # checks
        if not osp.exists(path):
            return False
        if osp.islink(path) or osp.ismount(path):
            return False

        try:
            fs_usr = int(self.cfg.get('DATADIRS', 'uid'))
            fs_grp = int(self.cfg.get('DATADIRS', 'gid'))
            fs_perm = int(self.cfg.get('DATADIRS', 'perm'), 8)
            self.LOG.info('setting permissions for: %s' % path)
            self.LOG.info('to %s %s %s' % (fs_usr, fs_grp, fs_perm))
            os.chmod(path, fs_perm)
            if fs_usr + fs_grp > 0:
                os.chown(path, fs_usr, fs_grp)
            self.log.info('permissions successfull set!')
        except Exception, ex:
            self.log.exception('could not set permissions: %s' % str(ex))
            return False
        return True

    @staticmethod
    def convert(cls, in_dict):
        """changes all ndarrays in a dict to lists (recursively)

        The ndarray.tolist() method is called, converting to a list of python
        base types.

        note:
            This methodod operates on a shallow copy of the dict passed. So
            changes to the contents are permanent and ireversable.

        :Parameters:
            in_dict: dict
                The dictionary to operate on.
        :Raises:
            TypeError : If in_dict is not a dict
        """

        if not isinstance(in_dict, dict):
            raise TypeError('input not a dict')

        for k in in_dict.keys():
            if isinstance(in_dict[k], dict):
                # recurse for dicts
                in_dict[k] = Evaluation.convert(in_dict[k])
            else:
                # try to convert ot list
                if isinstance(in_dict[k], ndarray):
                    in_dict[k] = in_dict[k].tolist()

        return in_dict


##--- MAIN

if __name__ == '__main__':
    pass
