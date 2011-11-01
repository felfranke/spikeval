# -*- coding: utf-8 -*-
#
# spikeval - datafiles.py
#
# Philipp Meier - <pmeier82 at gmail dot com>
# 2009-05-16
#

from __future__ import with_statement

"""reading spike trains from GDF and raw data from HDF5"""
__docformat__ = 'restructuredtext'
__all__ = ['read_gdf_sts', 'read_hdf5_arc', 'create_hdf5_arc']


##---IMPORTS

import scipy as sp
from tables import openFile
from util import dict_list2arr


##---FUNCTIONS

def read_gdf_sts(file_name):
    """reads a .gdf file and returns contents, mapping unit id to spike train

    :type file_name: str
    :param file_name: path to the file to read

    :returns: dict -- dict mapping unit id to the corresponding spike train
    """

    rval = {}
    with open(file_name, 'r') as arc:
        for line in arc:
            data = line.strip().split()
            if len(data) != 2:
                continue
            if data[0] not in rval:
                rval[data[0]] = []
            rval[data[0]].append(int(data[1]))
    return dict_list2arr(rval)


def read_hdf5_arc(file_name):
    """reads a .hdf file and returns data contents mapped in a dict

    :type file_name: str
    :param file_name: path to the file to read

    :returns: ndarray: raw data [f32], float: sampling rate in Hz,
    or None, None on read error
    """

    data, srate = None, None
    with openFile(file_name, 'r') as arc:
        for node in arc:
            # XXX: any more identifiers we used or the data in an archive?!
            if node._v_name.lower() in ['data', 'x']:
                data = sp.asanyarray(node.read())
                try:
                    data = data.astype(sp.float32)
                    if data.shape[0] <= data.shape[1]:
                        data = data.T.copy()
                except:
                    data = None
            if node._v_name.lower() == 'srate':
                try:
                    srate = float(node.read())
                except:
                    srate = None
    return data, srate


def create_hdf5_arc(file_name, rdata, srate=1000.0, **kwargs):
    """creates a valid hd5 archive for raw data storage

    :type file_name: str
    :param file_name: path to the file to read
    :type rdata: ndarray
    :param rdata: raw data array [samples, channels] castable to f32
    :type srate: float
    :param srate: sampling rate of rdata in Hz
        Default=1000.0

    :returns: True on success, False else
    """

    with openFile(file_name, 'w') as arc:
        # XXX: we go with 'data' here
        try:
            data = sp.asanyarray(rdata, dtype=sp.float32)
            if data.shape[0] <= rdata.shape[1]:
                data = data.T
            arc.createArray(arc.root, 'data', data)
            arc.createArray(arc.root, 'srate', srate)
            for k, v in kwargs.iteritems():
                arc.createArray(arc.root, str(k), v)
            return True
        except:
            return False

##---MAIN

if __name__ == '__main__':
    pass
