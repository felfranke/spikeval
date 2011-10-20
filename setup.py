# -*- coding: utf-8 -*-
#
# spikeval - setup.py
#
# Philipp Meier <pmeier82 at googlemail dot com>
# 2011-09-30
#

"""install script for the SpikeEval package"""
__author__ = 'Philipp Meier <pmeier82 at googlemail dot com>'
__docformat__ = 'restructuredtext'

from setuptools import setup, find_packages
import spikeval

DESC_TITLE = "SpikeEval : systematic evaluation of spike sorting"
DESC_LONG = ''.join([DESC_TITLE, '\n\n', open('README', 'r').read()])

if __name__ == "__main__":
    setup(name="spikeval",
          version=spikeval.__version__,
          packages=find_packages(),
          include_package_data=True,
          install_requires=[
              'scipy>=0.7.0',
              'matplotlib>=0.99.3',
              'spikeplot>=0.1.0',
              'tables>=2.1.2',
              'texttable>=0.8',
              'PIL>=1.1.7',
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
