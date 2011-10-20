# -*- coding: utf-8 -*-
#
# spikeval - module.base_module.py
#
# Philipp Meier <pmeier82 at googlemail dot com>
# 2011-09-29
#

"""result types for module results"""
__docformat__ = 'restructuredtext'
__all__ = ['ResultError']



##---IMPORTS

import scipy as sp
from texttable import Texttable
#from spikeplot import p


##---FUNCTIONS




##---CLASSES

class ResultError(ValueError):
    pass


class ModuleResult(object):
    """module result base class

    Module results can be arbitrarily complex, none the less they can be
    represented as a composition of results from a finite set of result
    types. Each result type implements this interface and provides methods
    to presented itself in various forms.
    """

    def __init__(self):
        self._value = None

    def __str__(self):
        s = self._str_val().splitlines()
        return '{0}{{{1}{2}{3}}}'.format(self.__class__.__name__,
                                         '\n' if len(s) > 1 else '',
                                         '\n'.join(s),
                                         '\n' if len(s) > 1 else '')

    def _str_val(self):
        return str(self._value)

    @property
    def value(self):
        return self._value


class MRScalar(ModuleResult):
    """single _value (scalar) result"""

    def __init__(self, value):
        """
        :type value: scalar dtype
        :param value: single digit _value
        """

        if not sp.isscalar(value):
            raise ValueError('%s is not a scalar!' % value)
        self._value = value


class MRTable(ModuleResult):
    """two dimensional table/matrix result"""

    def __init__(self, value, header=None):
        """
        :type value: ndarray
        :param value: single digit _value
        :type header: list
        :param header: list of str with as many entries as columns in _value
        """

        val = sp.asanyarray(value)
        if val.dtype == object:
            raise ValueError('%s is not a compatible type: %s' %
                             (value, value.__class__.__name__))
        if val.ndim != 2:
            raise ValueError('%s is not ndim==2: _value.ndim==%s' % val.ndim)
        self._value = val
        self.header = None
        if header is not None:
            if len(header) == self._value.shape[1]:
                self.header = map(str, header)

    @property
    def shape(self):
        return self._value.shape

    def _str_val(self):
        tt = Texttable()
        if self.header is not None:
            tt.header(self.header)
        tt.add_rows(self._value, header=False)
        return tt.draw()


class MRDict(ModuleResult):
    """dictionary result"""

    def __init__(self, init_values):
        """
        :type init_values: list
        :param init_values: list of tuples to initialise a dictionary from
        """

        self._value = dict(init_values)

    @property
    def shape(self):
        return self._value.shape

    def _str_val(self):
        tt = Texttable()
        tt.header(['Key', 'Value'])
        tt.add_rows(self._value.items(), header=False)
        return tt.draw()


class MRFigure(ModuleResult):
    """figure result"""

    # TODO: IMPLEMENT

    pass

##---MAIN

if __name__ == '__main__':
    res = ModuleResult()
    print res
    print

    res = MRScalar(5)
    print res
    print

    res = MRTable([[1, 0], [0, 1]])
    print res
    print res.shape
    print

    res = MRTable([[1, 0], [0, 1]], ['Abc', 'Bcd'])
    print res
    print res.shape
    print

    res = MRTable([[1, 2, 3]])
    print res
    print res.shape
    print

    res = MRDict(zip(range(10), map(chr, range(32, 45))))
    print res
    print
