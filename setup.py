#!/usr/bin/python3
#
# Copyright (c) 2017-2019 NVIDIA CORPORATION. All rights reserved.
# This file is part of webloader (see TBD).
# See the LICENSE file for licensing terms (BSD-style).
#

import sys
import setuptools

if sys.version_info < (3, 6):
    sys.exit("Python versions less than 3.6 are not supported")

VERSION = "0.0.2"

SCRIPTS = """
tar2tsv tarcats tsv2tar tarfirst tarmix
tarproc tarshow tarsort tarsplit tarpcat
""".split()

PREREQS = """
future
msgpack
braceexpand
simplejson
pyzmq
numpy
pyyaml
""".split()

setuptools.setup(
    name='tarproc',
    version=VERSION,
    description="Big data data processing for tar archives.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://github.com/tmbdev/webdataset",
    author="Thomas Breuel",
    author_email="tmbdev+removeme@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
    keywords="POSIX tar, map reduce, object store, deep learning",
    packages=["tarproclib"],
    python_requires=">=3.6",
    scripts=SCRIPTS,
    install_requires=PREREQS,
)
