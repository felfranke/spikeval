# -*- coding: utf-8 -*-
#
# spikeval - util.py
#
# Philipp Meier <pmeier82 at googlemail dot com>
# 2011-09-28
#

"""general tools for dictionary and array handling"""
__author__ = 'Philipp Meier <pmeier82 at googlemail dot com>'
__docformat__ = 'restructuredtext'
__all__ = ['dict_list2arr', 'dict_arrsort']


##---IMPORTS

import scipy as sp


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

##---MAIN

if __name__ == '__main__':
    pass
