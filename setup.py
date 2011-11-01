# -*- coding: utf-8 -*-
#
# spikeval - setup.py
#
# Philipp Meier <pmeier82 at googlemail dot com>
# 2011-09-30
#

"""install script for the SpikEval package"""
__author__ = 'Philipp Meier <pmeier82 at googlemail dot com>'
__docformat__ = 'restructuredtext'

from setuptools import setup, find_packages

def find_version():
    """read version from __init__"""
    rval = '-1'
    with open('./spikeval/__init__.py', 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                rval = line.split()[-1][1:-1]
                break
    return rval

DESC_TITLE = "SpikEval : systematic evaluation of spike sorting"
DESC_LONG = ''.join([DESC_TITLE, '\n\n', open('README', 'r').read()])
VERSION = find_version()

if __name__ == "__main__":
    setup(name="spikeval",
          version=VERSION,
          packages=find_packages(),
          include_package_data=True,
          install_requires=[
              'scipy>=0.7.0',
              'matplotlib>=0.98',
              'spikeplot>=0.1.0',
              'tables>=2.0',
              'texttable>=0.8',
              'PIL>=1.1.6',
              'mdp>=3.1',
              ],
          requires=[],

          # metadata for upload to PyPI
          author="Philipp Meier",
          author_email="pmeier82@googlemail.com",
          maintainer="Philipp Meier",
          maintainer_email="pmeier82@googlemail.com",
          description=DESC_TITLE,
          long_description=DESC_LONG,
          license="EUPL v1.1",
          url='http://ni.tu-berlin.de',
          classifiers=[
              'Development Status :: 4 - Beta',
              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',
              'Intended Audience :: Education',
              'License :: OSI Approved :: MIT License',
              'Natural Language :: English',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Topic :: Scientific/Engineering :: Bio-Informatics',
              'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
              ])
