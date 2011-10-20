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
import copy


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
        self.value = None

    def __str__(self):
        s = self._str_val().splitlines()
        return '{0}{{{1}{2}{3}}}'.format(self.__class__.__name__,
                                         '\n' if len(s) > 1 else '',
                                         '\n'.join(s),
                                         '\n' if len(s) > 1 else '')

    def _str_val(self):
        return str(self.value)


class MRScalar(ModuleResult):
    """single value (scalar) result"""

    def __init__(self, value):
        """
        :type value: scalar dtype
        :param value: single digit value
        :return:
        """

        if not sp.isscalar(value):
            raise ValueError('%s is not a scalar!' % value)
        self.value = value


class MRTable(ModuleResult):
    """single value (scalar) result"""

    def __init__(self, value, header=None):
        """
        :type value: ndarray
        :param value: single digit value
        :return:
        """

        val = sp.asanyarray(value)
        if val.dtype == object:
            raise ValueError('%s is not a compatible type: %s' %
                             (value, value.__class__.__name__))
        if val.ndim != 2:
            raise ValueError('%s is not ndim==2: value.ndim==%s' % val.ndim)
        self.value = val
        self.header = None
        if header is not None:
            if len(header) == self.value.shape[1]:
                self.header = map(str, header)

    @property
    def shape(self):
        return self.value.shape

    def _str_val(self):
        if self.header is None:
            rval = super(MRTable, self)._str_val()
        else:
            from pretty_print import indent

            table_rows = [self.header]
            for row in self.value:
                table_rows.append(map(str,row))
            rval = indent(table_rows, hasHeader=True)
        return  rval

##---MAIN

if __name__ == '__main__':
    res = ModuleResult()
    print res

    res = MRScalar(5)
    print res

    res = MRTable([[1, 0], [0, 1]])
    print res
    print res.shape

    res = MRTable([[1, 0], [0, 1]], ['Abc', 'Bcd'])
    print res
    print res.shape
