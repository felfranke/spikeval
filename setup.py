# -*- coding: utf-8 -*-
#
# spikeval - setup.py
#
# Philipp Meier <pmeier82 at googlemail dot com>
# 2011-09-30
#

from setuptools import setup

DESC_TITLE = "SpikEval : systematic evaluation of spike sorting results"
DESC_LONG = ''.join([DESC_TITLE, '\n\n', open('README', 'r').read()])
VERSION = __import__("spikeval").__version__

if __name__ == "__main__":
    setup(
        name="spikeval",
        version=VERSION,

        description=DESC_TITLE,
        long_description=DESC_LONG,

        url="https://github.com/pmeier82/SpikeEval",
        license="BSD",
        author="Philipp Meier",
        author_email="pmeier82@gmail.com",

        install_requires=["scipy", "texttable", "tables"],
        packages=["spikeval"],

        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Scientific/Engineering :: Bio-Informatics",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
        ])
