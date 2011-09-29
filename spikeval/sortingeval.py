__docformat__ = 'restructuredtext'
__version__ = '0.5'


#--- IMPORTS

# builtins
import   os.path as osp
# packages
# spike
from evalplots import do_plotting
from file_types import read_file
from common import align_spike_trains


def sorting_eval(data_dir, ev_file, base_dir, gt_file, result_dir, log=None):
    if log is None:
        log = dummy_log

    # read in evaluation file
    log('*-reading files')
    train = read_file(osp.join(data_dir, ev_file))
    log('evaluation file read!')

    benchmark = gt_file
    log("gtfile:")
    log(gt_file)
    log(" benchmark: ")
    log(benchmark)
    bm_filename = osp.join(base_dir, benchmark)
    log('groundtruth file found: %s' % bm_filename)
    groundtruth = read_file(bm_filename)
    log('groundtruth file read!')

    # calculate alignment
    log('*-evaluation of data')
    results = align_spike_trains(
        groundtruth,
        train,
        max_shift=35
    )

    log('evaluation done!')

    # generate charts
    log('*-generating plots')

    do_plotting(
        result_dir,
        bm_filename,
        train,
        results['delta_shift'],
        ev_file.split('.')[0]
    )
    log('plots done!')

    rval = {'results': results, 'train': train, 'benchmark': benchmark}
    return rval


def dummy_log(dummy):
    print dummy
    pass


##--- MAIN
if __name__ == '__main__':
    sorting_eval(r'/www/eval/application/python',
                 r'021_C_Easy1_noise01.gdf',
                 r'/www/eval/groundtruth',
                 r'C_Easy1_noise005_groundtruth.mat',
                 r'/www/eval/application/python/results')
