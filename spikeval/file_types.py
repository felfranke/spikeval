# -*- coding: utf-8 -*-
#
# eval - filetypes.py
#
# Philipp Meier - <pmeier82 at gmail dot com>
# 2009-05-16
#

"""readers for various file types. [GDF, HDF5, MAT, NEX]"""
__docformat__ = 'restructuredtext'


##--- IMPORTS

import struct
import scipy as sp
from scipy.io import loadmat
from h5py import File


##--- FUNCTIONS

def read_file(file_name):
    """convenience function delgating to the correct read_<ext> function

    @type file_name: string[path]
    @param file_name: path to the filename

    @rtype: dict of numpy.ndarray
    @return: the files contents

    @raise ValueError: unknown filetype, known: .gdf, .mat, .nex
    @raise IOError: problem reading the file"""

    ext = file_name.split('.')[-1].lower()
    # HERE: adjust for new filetypes
    if ext == 'gdf':
        return read_gdf(file_name)
    elif ext == 'mat':
        return read_mat(file_name)
    elif ext == 'nex':
        return read_nex(file_name)
    elif ext == 'hdf5':
        return read_hdf5(file_name)
    else:
        raise ValueError('unknown filetype for file: %s' % file_name)


def read_gdf(file_name):
    """
    reads a .gdf file and stores to a dict

    Seems gdfs can only be read sequentially, so we read in line-wise and store
    to lists (one list per unit). After reading we convert each list to
    C{numpy.ndarray}.

    @type file_name: string[path]
    @param file_name: path to the file to read

    @rtype: dict of numpy.ndarray
    @return: one sequence per unit
    """

    rval = {}
    read_file = open(file_name, 'r')

    for line in read_file:
        data = line.strip().split()
        if len(data) != 2:
            continue
        if data[0] not in rval:
            rval[data[0]] = []
        rval[data[0]].append(int(data[1]))
    read_file.close()

    for k in rval.keys():
        rval[k] = sp.array(rval[k])

    return rval


def read_mat(file_name):
    """reads a .mat file and stores the var named 'spiketrains' to a dict.

    @type file_name: string[path]
    @param file_name: path to the file to read

    @rtype: dict of numpy.ndarray
    @return: one sequence per unit"""

    # try to handle old .mat files
    try:
        arc = loadmat(file_name)
        if 'spiketrains' not in arc:
            raise ValueError('no variable named \'spiketrains\' found!')
        return st2dict(arc['spiketrains'])
    except:
        # try to handle new hdf5 .mat files
        rval = read_hdf5(file_name)
        return rval


def read_hdf5(file_name):
    """reads a .hdf file and stores neuron timeseries data to a dictionary

    Read all variables in the .mat file and assumes they are timeseries data
    for neurons.

    @type file_name: string[path]
    @param file_name: path to the file to read

    @rtype: dict of numpy.ndarray
    @return: one sequence per unit"""

    arc = File(file_name, 'r')
    if 'spiketrains' not in arc:
        raise ValueError('no variable named \'spiketrains\' found!')
    return st2dict(arc['spiketrains'])


def read_nex(file_name):
    """reads a .nex file and stores neuron timeseries data to a dictionary

    .nex format can store lots of datatypes, we are only interested in timeline
    data for a neuron.

    @type file_name: string[path]
    @param file_name: path to the file to read

    @rtype: dict of numpy.ndarray
    @return: one sequence per unit"""

    rval = {}
    f = open(file_name, 'rb')
    # check for nex file
    raw = f.read(8)
    magic, ver = struct.unpack('4si', raw)
    assert magic == 'NEX1', 'not a nex file'
    assert ver == 100, 'not version 1.0'
    # read file header
    f.seek(0)
    raw = f.read(544)
    values = struct.unpack('4si256sdiiii256s', raw)
    fh = dict(zip(['magic',
                   'version',
                   'comment',
                   'freq',
                   'start',
                   'end',
                   'vars',
                   'next',
                   'padding'],
                             values))
    fh['comment'] = fh['comment'].split('\x00')[0]
    assert fh['vars'] > 0, 'no variables'
    # read variable headers
    vhs = []
    for _ in xrange(fh['vars']):
        raw = f.read(208)
        values = struct.unpack('ii64siiiiiiddddiii68s', raw)
        vh = dict(zip(['type',
                       'version',
                       'name',
                       'offset',
                       'count',
                       'wire_no',
                       'unit_no',
                       'gain',
                       'filter',
                       'xpos',
                       'ypos',
                       'wfreq',
                       'ad2mv',
                       'points_per_wave',
                       'markers',
                       'marker_len',
                       'padding'],
                                 values))
        vh['name'] = vh['name'].split('\x00')[0]
        vhs.append(vh)
        # look for neuron timeseries and save them
    for var in vhs:
        if var['type'] != 0:
            continue
        f.seek(var['offset'])
        raw = f.read(var['count'] * 4)
        rval[var['name']] = sp.array(list(struct.unpack('%si' % var['count'],
                                                        raw)))
        # return
    f.close()
    return rval


##---HELPERS

def st2dict(train):
    """converts the 'spiketrains' to a dict conform to the C{evaluate}
    routine"""

    # checks and inits
    rval = {}
    if train.shape[0] != 2:
        train = train.T

    # build dict
    for i in xrange(train.shape[1]):
        if int(train[0, i]) not in rval:
            rval[int(train[0, i])] = []
        rval[int(train[0, i])].append(int(train[1, i]))

    # convert to arrays
    for k in rval:
        rval[k] = sp.asarray(rval[k])

    # return
    return rval


##---MAIN

if __name__ == '__main__':
    pass
