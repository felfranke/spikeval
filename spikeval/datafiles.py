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


##---IMPORTS

from tables import openFile
from util import dict_list2arr


##---FUNCTIONS

def read_gdf(file_name):
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


def read_hdf5(file_name):
    """reads a .hdf file and returns data contents mapped in a dict

    :type file_name: str
    :param file_name: path to the file to read

    :returns: dict -- dict mapping hdf5 name to numpy.ndarray content
    """

    rval = {}
    with openFile(file_name, 'r') as arc:
        for node in arc:
            if node._v_name in ['data', 'units']:
                rval[str(node._v_name)] = node.read()
    if len(rval) == 0:
        raise IOError('no node with name "data" or "units" was found in the '
                      'archive!')
    return rval


##---MAIN

if __name__ == '__main__':
    pass
