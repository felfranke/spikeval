# -*- coding: utf-8 -*-
#
# spikeval - util.py
#
# Philipp Meier <pmeier82 at googlemail dot com>
# 2011-09-28
#

"""general utility/tools for dictionary and array handling"""
__docformat__ = 'restructuredtext'
__all__ = ['dict_list2arr', 'dict_arrsort']


##---IMPORTS

import scipy as sp


##---EXCEPTIONS

class UtilException(Exception):
    pass

##---FUNCTIONS

def dict_list2arr(in_dict):
    """converts all lists in a dictionary to `ndarray`.

    If there are instances of dict found as values, this function will be
    applied recursively.

    :Parameters:
        in_dict : dict
    """

    try:
        for k in in_dict:
            if isinstance(in_dict[k], list):
                in_dict[k] = sp.asanyarray(in_dict[k])
            elif isinstance(in_dict[k], dict):
                dict_list2arr(in_dict[k])
            else:
                pass
    finally:
        return in_dict


def dict_arrsort(in_dict):
    """sort all arrays in a dictionary"""

    try:
        for k in in_dict.keys():
            if isinstance(in_dict[k], sp.ndarray):
                in_dict[k] = sp.sort(in_dict[k])
    finally:
        return in_dict


def extract_spikes(data, epochs):
    """extract spike waveforms according to :epochs: from :data:

    :type data: ndarray
    :param data: the signal to extract from [samples, channels]
    :type epochs: ndarray
    :param epochs: epochs to cut [[start,end]], should have common length!
    :type mc: bool
    :returns: ndarray, extracted spike waveforms from :data:
    """

    # inits and checks
    if not all(map(isinstance, [data, epochs], [sp.ndarray] * 2)):
        raise TypeError('pass sp.ndarrays!')
    ns, nc = epochs.shape[0], data.shape[1]
    if epochs.shape[0] == 0:
        return sp.zeros((0, 0))
    tf = epochs[0, 1] - epochs[0, 0]

    # extract
    rval = sp.zeros((ns, tf * nc), dtype=data.dtype)
    for s in xrange(ns):
        for c in xrange(nc):
            start = max(0, epochs[s, 0])
            correct_end = max(0, epochs[s, 1] - data.shape[0])
            rval[s, c * tf + cor_s:(c + 1) * tf - correct_end] =\
            data[start:epochs[s1] - correct_end, c]
    return rval

##---MAIN

if __name__ == '__main__':
    pass
