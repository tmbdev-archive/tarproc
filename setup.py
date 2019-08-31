#!/usr/bin/python3
#
# Copyright (c) 2017-2019 NVIDIA CORPORATION. All rights reserved.
# This file is part of webloader (see TBD).
# See the LICENSE file for licensing terms (BSD-style).
#

from __future__ import print_function

import sys
import glob
from distutils.core import setup  # , Extension, Command

if sys.version_info < (3, 6):
    sys.exit("Python versions less than 3.6 are not supported")

scripts="""
tar2tsv tarcat tarcreate tarfirst
tarproc tarshow tarsort tarsplit tarpcat
""".split()

prereqs = """
    braceexpand
    simplejson
""".split()

setup(
    name='tarproclib',
    version='v0.0',
    author="Thomas Breuel",
    description="Big data data processing for tar archive.",
    packages=["tarproclib"],
    scripts=scripts,
    install_requires=prereqs,
)
