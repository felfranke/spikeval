# -*- coding: utf-8 -*-
#
# spikeval - module.mod_metric_franke.py
#
# Maria Meila <mmp@stat.washington.com>
# <ref>
#
# adjusted for spikeval by Philipp Meier, Oct. 2012
#

"""spike train metric using variation of information"""
__docformat__ = 'restructuredtext'
__all__ = ['ModMetricMeila']


##--- IMPORTS

import scipy as sp
from .base_module import BaseModule, ModuleInputError, ModuleExecutionError
from .result_types import MRScalar
from ..util import dict_arrsort, dict_list2arr, matrix_argmax

##---CLASSES

class ModMetricMeila(BaseModule):
    """module: metric for spike train alignment

    computes the evaluation of spike sorting

    self.sts_ev contains the sorted spike trains - given the
    real/ideal/ground truth spike trains in self.sts_gt

    <description of method>

    :Parameters:
        self.sts_gt : dict of ndarray
            dict containing 1d ndarrays/lists of integers, representing the
            single unit spike trains. This is the ground truth.
        self.sts_ev : dict of ndarray
            dict containing 1d ndarrays/lists of integers, representing the
            single unit spike trains. this is the estimation.
    """

    # module interface

    RESULT_TYPES = [
        MRScalar, # result
    ]

    def _check_sts_gt(self, sts_gt):
        if sts_gt is None:
            raise ModuleInputError('sts_gt: '
                                   'needs ground truth spike train set')
        dict_list2arr(sts_gt)
        dict_arrsort(sts_gt)
        return sts_gt

    def _check_sts_ev(self, sts_ev):
        if sts_ev is None:
            raise ModuleInputError('sts_ev: '
                                   'needs evaluation spike train set')
        dict_list2arr(sts_ev)
        dict_arrsort(sts_ev)
        return sts_ev

    def _check_parameters(self, parameters):
        return {
            'sampling_rate': parameters.get('sampling_rate', 32000.0),
            'name': parameters.get('name', 'noname'), }

    def _apply(self):
        # init and checks
        n = len(self.sts_gt)
        m = len(self.sts_ev)
        rval = 0.0


        # return results
        self.result = [
            MRScalar(rval), # result
        ]

    @staticmethod
    def entropy(x):
        """compute entropy of a discrete random variable"""

        return -sp.nansum(x * sp.log(x))

    @staticmethod
    def mutual_information(x, y, xy):
        """compute mutual information between the associated random variables"""

        # init
        MI = sp.zeros(x.size, y.size)

        for i in xrange(x.size):
            for j in xrange(y.size):
                MI[i, j] = xy[i, j] * sp.log(xy[i, j] / (x[i] * y[j]))

        # return
        return sp.nansum(MI)

    @staticmethod
    def vi_metric(confmx):
        """computes Marina Meila's variation of information metric between two clusterings of the same data"""

        # init
        rval = {'MI': None, 'VI': None, 'Px': None, 'Py': None, 'Pxy': None, 'Hx': None, 'Hy': None}
        nx, ny = confmx.shape
        Px = sp.zeros(nx)
        Py = sp.zeros(ny)

        # compute
        tot = sp.nansum(confmx)
        for i in xrange(nx):
            Px[i] = confmx[i, :].sum() / tot
        for j in xrange(ny):
            Py[j] = confmx[:, j].sum() / tot
        Pxy = confmx / tot
        Hx = ModMetricMeila.entropy(Px)
        Hy = ModMetricMeila.entropy(Py)
        MI = ModMetricMeila.mutual_information(Px, Py, Pxy)

        # return
        rval['VI'] = Hx + Hy - 2 * MI
        rval['MI'] = MI
        rval['Pxy'] = Pxy
        rval['Px'] = Px
        rval['Py'] = Py
        rval['Hx'] = Hx
        rval['Hy'] = Hy
        return rval

    @staticmethod
    def confmx(gt, ev):
        """returns confusion matrix of sorting A and B"""

        pass

##--- MAIN

if __name__ == '__main__':
    pass
