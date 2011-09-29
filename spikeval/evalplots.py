# -*- coding: utf-8 -*-
#
# spikeval - evalplots.py
#
# Philipp Meier <pmeier82 at googlemail dot com>
# 2011-09-29
#

"""plots for evaluation"""
__author__ = 'Philipp Meier <pmeier82 at googlemail dot com>'
__docformat__ = 'restructuredtext'


##--- IMPORTS

import sys
from os.path import join
from h5py import File
import scipy as N
from scipy.io import loadmat
import plot


##--- FUNCTIONS

def do_plotting(save_dir, data_file, events, delta_shift, name='none'):
    """produces all plots to the desired dir for the passed data

    :Parameters:
    save_dir : path
        dir where the plots are saved
    data_file : path
        data archive (from simulator)
    events : dict
        timeseries data for the units
    name : string
        name for the chart title
    """

    # read archive and get administrative parameters
    arc = None
    X = None
    cut = None
    NC = None
    srate = None
    try:
        # assume hdf5
        arc = File(data_file, 'r')
        X = arc['X'].value
        cut = arc['plt/templateLengthSamples'][0, 0]
        srate = arc['plt/sampleRate'][0, 0]
        NC = arc['C'].value
        arc.close()
        del arc
    except:
        try:
            # try old .mat file
            arc = loadmat(data_file)
            X = arc['X'].T

            # check the archive since Scipy 0.6 handles matlab files differently then Scipy 0.7!
            if isinstance(arc['plt'], N.ndarray):
                # new scipy:
                cut = arc['plt'][0, 0].templateLengthSamples[0, 0]
                srate = arc['plt'][0, 0].sampleRate[0, 0]
            else:
                # old scipy on tairach:
                cut = arc['plt'].templateLengthSamples
                srate = arc['plt'].sampleRate
                # add second dimension on tairach since the old scipy loads 1D arrays
                X = N.atleast_2d(X)

            NC = arc['C']
            del arc
        except Exception, ex:
            raise ValueError(
                'cannot open groundtruth file: %s,\n reason: %s' %
                (data_file, ex)
            )
    n, chans = X.shape
    if chans > n:
        X = X.T
        n, chans = X.shape
    cutLeft = N.ceil(cut / 2.5)
    cutRight = cut - cutLeft
    # extract the spikes and concatenate across the channels
    spikes = {}
    # cut spikes exactly as user thinks, therefor do not change the user
    # supplied events for spike extraction
    #for i in xrange(len(events)):
    #    events[events.keys()[i]] += delta_shift[i]
    for k in sorted(events.keys()):
        train = events[k][(events[k] > cutLeft) * (events[k] < n - cutRight)]
        epochs = N.vstack((
            train - cutLeft,
            train + cutRight
            )).T
        i_spikes = U.extract_spikes(X, epochs)
        spikes[k] = i_spikes

    # close file and plot stuff
    plot_waveforms(save_dir, spikes, name=name, cut=cut)
    plot_clustering(save_dir, spikes, name=name, NC=NC)
    plot_spiketrain(save_dir, events, name=name, srate=srate)


def plot_spiketrain(save_dir, events, name='none', srate=32000):
    """spiketrain plot

    :Parameters:
        save_dir : path
            save_dir: dir where the plots are saved
        events : dict
            events: spike trains
        srate : int
            srate: sampling rate in
        name : string
            name for the chart title
    """

    # setup stuff
    fig = P.figure()
    fig.set_figheight(1 + .25 * len(events))
    fig.set_figwidth(7.5)
    left = .15
    bottom = .2
    width = .83
    height = .78
    ax = fig.add_axes([left, bottom, width, height])

    fname = join(save_dir, ''.join([name, '_spiketrain']))

    plot.spike_trains(
        events,
        plot_handle=ax,
        samples_per_second=srate,
        show=0,
        filename=fname, marker_width=1
    )


def plot_waveforms(save_dir, spikes, name='none', cut=60):
    """produces plots of waveforms

    There will be one plot per unit and one plot with all units, each plot just
    stacks the extracted spike waveforms (concatenated over the channels).

    :Parameters:
        save_dir : path
            save_dir: dir where the plots are saved
        spikes : dict
            data_file: the extracted spike waveforms, one ndarray per unit
            (possibly concatenated across the channels)
        name : string
            name: name for the chart title
    """

    # setup stuff
    col_idx = 0

    # produce plots for every unit ...
    for k in sorted(spikes.keys()):
        fname = join(save_dir, ''.join([name, '_wf-', str(k)]))
        plot.waveforms(spikes[k],
                       tf=cut,
                       plot_mean=0,
                       title='Waveforms for unit %s' % (k),
                       colors=[COLORS[col_idx]],
                       show=0,
                       filename=fname)
        col_idx += 1

    # ... with all spikes ...
    fname = join(save_dir, ''.join([name, '_wf-all']))
    plot.waveforms(
        spikes,
        tf=cut,
        plot_mean=0,
        title='All waveforms',
        show=0,
        filename=fname
    )

    # ... and of the mean waveforms
    fname = join(save_dir, ''.join([name, '_wf-mean']))
    plot.waveforms(
        spikes,
        tf=cut,
        plot_mean=1,
        plot_single_waveforms=0,
        title='waveforms all templates',
        show=0,
        filename=fname
    )


def plot_clustering(save_dir, spikes, name='none', NC=None):
    """produces plots visualizing the clustering

    There will be one plot showing the clustering of units (scatter plot using
    the first two principal components). The initial clustering is preserved as
    colorization in the projected data.

    Also there will be a plot showing the projection of each cluster pairing
    onto the vector connecting the corresponding cluster means.

    :Parameters:
    save_dir: path
        save_dir: dir where the plots are saved
    spikes: dict
        data_file: the extracted spike waveforms, one ndarray per unit
        (possibly concatenated across the channels)
    name: string
        name for the chart title
    """

    # setup
    data, iU, cholNC = U.prewhiten(spikes, NC)

    PC, V, pca_data, explained = U.princomp(data, explain=4)

    # produce scatter plots
    for pc in [(0, 1), (2, 3)]:
        # setup
        fname = join(save_dir, ''.join([name, '_scatter-%s%s' %
                                              (pc[0] + 1, pc[1] + 1)]))
        plot.clusters(
            pca_data,
            data_dim=pc,
            plot_mean=1,
            title='scatter plot for: %s' % name,
            xlabel='PC%s' % (pc[0] + 1), ylabel='PC%s' % (pc[1] + 1),
            show=0,
            filename=fname
        )

    # CLUSTER CENTER PROJECTIONS
    fname = join(save_dir, ''.join([name, '_projection']))
    plot.cluster_projections(data, show=0, filename=fname)


##--- MAIN

if __name__ == '__main__':
    pass
