#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# spikeval - launch
#
# Philipp Meier - <pmeier82 at gmail dot com>
# 2009-05-15
#
# $Id: launch.py 4796 2010-05-21 15:25:58Z ff $
#

"""
script to launch the evaluation website backend

This script is called by the website to process a new evaluation-job requests.
It will run until it cannot find more jobs that need processing, which is
indicated by job's status in the 'jobqueue' table of the evaluation database.

This script requires a valid 'spikeval.cfg' in the SAME directory it is called
from!
"""
from __future__ import with_statement

__docformat__ = 'restructuredtext en'


##--- IMPORTS

# builtins
from ConfigParser import ConfigParser
import logging, os, sys, os.path as osp
import logging.handlers
# packages
import MySQLdb
# own packages
from evaluation import Evaluation


##--- LOGGER

LOG = logging.getLogger('spikeval')
LOG.setLevel(logging.DEBUG)

SQLLOG = logging.getLogger('spikeval_sql')
SQLLOG.setLevel(logging.DEBUG)

##---CONSTANTS

PENDING_STATUS = [0]
CFG_FILE = '../../configs/spikeval.cfg'


##---FUNCTIONS
def sql_query_str(db, query):
    rval = None
    res = sql_query(db, query)
    if res is not None and len(res) > 0:
        rval = str(res[0][0])
    return rval


def sql_query(db, query):
    # check
    if not isinstance(db, MySQLdb.connection):
        raise TypeError('db is no connection object!')

    try:
        LOG.info('SQL Query...')
        cur = db.cursor()
        SQLLOG.info(query)
        cur.execute(query)
        rval = cur.fetchall()
        db.commit()
    except Exception, ex:
        LOG.error('Error while executing sql query: %s' % query)
        LOG.exception(ex)
    finally:
        cur.close()
    return rval


def create_logger(cfg):
    #build logger info/debug
    log_handler = logging.handlers.RotatingFileHandler(
        cfg.get('LOGGING', 'log_file'),
        maxBytes=cfg.get('LOGGING', 'log_maxbytes'),
        backupCount=cfg.get('LOGGING', 'log_nbackups')
    )
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    )
    LOG.addHandler(log_handler)
    #build logger sql
    sql_log_handler = logging.handlers.RotatingFileHandler(
        cfg.get('LOGGING', 'sql_log_file'),
        maxBytes=cfg.get('LOGGING', 'log_maxbytes'),
        backupCount=cfg.get('LOGGING', 'log_nbackups')
    )
    sql_log_handler.setLevel(logging.DEBUG)
    sql_log_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    )
    SQLLOG.addHandler(sql_log_handler)


def yield_new_job(db):
    """test if there are jobs waiting

    This function queries the database for new jobs and returns the first key
    that needs processing it finds. Key should be a string of the unique
    identifier for that job, also the directory name where to look for the
    job's data.

    :Parameters:
        db : MySQLdb connection
            The db connection
    :Returns:
        key : None or string
            Either the key for a job to process, 'None' else.
    """

    if len(PENDING_STATUS) > 1:
        pend_stat = str(tuple(PENDING_STATUS))
    else:
        pend_stat = '(' + str(PENDING_STATUS[0]) + ')'

    THE_QUERY = """
        SELECT uid
        FROM upload
        WHERE status IN %s
        ORDER BY time
        LIMIT 1
    """ % pend_stat
    rval = sql_query_str(db, THE_QUERY)
    if rval is None:
        LOG.info('found no job key')
    else:
        LOG.info('found job key: %s' % rval)
    return rval


def set_job_status(db, key, status, comment=''):
    """set the status for a job in the db

    :Parameters:
        db : MySQLdb.connection
            DB handle
        key : str
            key of the job to set the status on
        status : int
            index of the status to set
        comment : str
            String for the error/comment if needed.
    :Raises:
        TypeError : If db si corrupt.
    """

    # check
    if not isinstance(db, MySQLdb.connection):
        raise TypeError('db is no connection object!')

    LOG.info('want to change job status: %s->%d, %s' % (key, status, comment))

    THE_QUERY = """
        UPDATE upload
        SET status = '%d', status_comment = "%s"
        WHERE uid = "%s"
    """ % (status, comment, key)
    # TODO: adjust query! we want to set the status in jobqueue based on the
    #       string key of the job.
    sql_query(db, THE_QUERY)


def set_job_status_at_least_to(db, key, status, comment=''):
    """set the status for a job in the db

    :Parameters:
        db : MySQLdb.connection
            DB handle
        key : str
            key of the job to set the status on
        status : int
            index of the status to set
        comment : str
            String for the error/comment if needed.
    :Raises:
        TypeError : If db si corrupt.
    """

    # check
    if not isinstance(db, MySQLdb.connection):
        raise TypeError('db is no connection object!')

    LOG.info('want to change job status at least to: %s->%d, %s' % (key, status, comment))

    THE_QUERY = """
        UPDATE upload
        SET status = '%d', status_comment = "%s"
        WHERE uid = "%s"
    """ % (status, comment, key)
    # TODO: adjust query! we want to set the status in jobqueue based on the
    #       string key of the job.
    sql_query(db, THE_QUERY)


def set_file_status(db, key, filename, comment):
    """set the status for a file in the db

    :Parameters:
        db : MySQLdb.connection
            DB handle
        key : str
            key of the job to set the status on
        filename : str
            filename
        comment : str
            String for the error/comment if needed.
    :Raises:
        TypeError : If db is corrupt.
    """

    # check
    if not isinstance(db, MySQLdb.connection):
        raise TypeError('db is no connection object!')

    # db stuff
    LOG.info(
        'want to change file status for: %s->%s %s' %
        (key, filename, comment)
    )
    THE_QUERY = """
        UPDATE uploadfile
        SET status_comment = "%s"
        WHERE uid = '%s' AND filename = "%s"
    """ % (comment, key, filename)
    # TODO: adjust query! we want to set the status in jobqueue based on the
    #       string key of the job.
    sql_query(db, THE_QUERY)


##--- MAIN

def main():
    """main entry point

    :Returns:
        None on success, a string with the exeption on failure.
    """

    try:
        # read config file
        cfg = ConfigParser()
        cfg_check = cfg.read(CFG_FILE)
        if CFG_FILE not in cfg_check:
            raise ValueError('could not load config file from %s' % CFG_FILE)

        create_logger(cfg)
        PID_FILE = cfg.get('LOGGING', 'pid_file')

        LOG.info('#-launch.py called')

        # pid file check
        LOG.info('checking for pid file..')
        if os.path.exists(PID_FILE):
            pid = None
            with open(PID_FILE, 'r') as pidfile:
                pid = pidfile.read()
            if pid is None:
                os.remove(PID_FILE)
            else:
                try:
                    os.kill(int(pid), 0)
                except OSError:
                    os.remove(PID_FILE)
                else:
                    LOG.info('pif file exits->terminating!')
                    raise RuntimeError('other spikeval already running!')
        with open(PID_FILE, 'w') as pfile:
            pfile.write(str(os.getpid()))
            LOG.info('created pid file!')

        # create db con
        LOG.info('creating db connection..')
        db = MySQLdb.connect(
            host=cfg.get('DATABASE', 'dbhost'),
            db=cfg.get('DATABASE', 'dbname'),
            user=cfg.get('DATABASE', 'dbuser'),
            passwd=cfg.get('DATABASE', 'dbpswd')
        )
        LOG.info('db connection created!')

        # jobs loop
        done = False
        max_iter = 100
        iter = 0
        while done is not True and iter < max_iter:
            iter += 1
            try:
                # get key
                key = yield_new_job(db)
                if key is None:
                    done = True
                    continue

                # process key
                LOG.info('#-starting job: %s' % key)
                set_job_status(db, key, 1)
                job_is_ok = True

                # eval per file
                jobdir = os.path.join(cfg.get('DATADIRS', 'ul_dir'), key)
                for f in os.listdir(jobdir):
                    try:
                        if not os.path.isdir(os.path.join(jobdir, f)):
                            LOG.info('starting file %s for job %s' % (f, key))
                            base_dir = cfg.get('DATADIRS', 'gt_dir')
                            gt_file = get_filename(key, f, base_dir, db, LOG)

                            job = Evaluation(key, cfg, f, gt_file, LOG)
                            # No threading on windows machines
                            if os.name == 'nt':
                                job.process()
                            else:
                                job.start()
                                job.join()

                            del job
                    except Exception, ex:
                        LOG.exception(ex)
                        set_file_status(db, key, f, str(ex))
                        job_is_ok = False

                # status update
                if job_is_ok is True:
                    set_job_status_at_least_to(db, key, 10, 'ok')
                else:
                    set_job_status(db, key, 9, 'minor problem')
            except Exception, ex:
                LOG.exception(ex)
                set_job_status(db, key, 9, str(ex))
    except Exception, ex:
        LOG.exception(ex)
        sys.exit(str(ex))
    else:
        sys.exit(0)
    finally:
        try:
            db.close()
        except:
            pass
        try:
            os.remove(PID_FILE)
        except:
            pass


def get_filename(key, filename, basedir, db, LOG):
    """yields a filename from a directory matching the name passed

    It is assumed the name passed is of shape: <id1>_<id2>_<any>.<ext>. The
    returned filename is the first match like <id1>_<id2>_<any>, with any
    filetype extension.

    :Parameters:
        filename : string
            name of the file to check for
    :Raises:
        AssertionError : if the directory does not exist, is empty or
            name is not of the shape described above
        ValueError : if no match was found
        MySQLdbError : if problemlem with the db
    """

    # the query
    THEQUERY = """
            SELECT
                df.groundtruth
            FROM
                datafile as df,
                uploadfile as uf
            WHERE
                uf.UID = '%s'
                AND uf.filename = '%s'
                AND df.ID = uf.datafileid
        """ % (key, filename)

    # query db for the filename
    name = None
    try:
        # mysql config
        cur = db.cursor()
        cur.execute(THEQUERY)
        name = cur.fetchall()[0][0]
    except Exception, ex:
        LOG.exception(ex)
    finally:
        cur.close()

    # check for file
    if not osp.exists(basedir) or not osp.isdir(basedir):
        raise ValueError('couldn\'t find basedir (%s)' % basedir)
    if len(os.listdir(basedir)) < 1:
        raise ValueError('no files in basedir (%s)' % basedir)
    if name is None or name is '':
        raise ValueError('no matching file found (name=%s)' % name)

    for item in os.listdir(basedir):
        if name in item:
            return item
    raise ValueError('no matching file found (name=%s)' % name)


if __name__ == '__main__':
    main()
