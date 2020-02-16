#
# Copyright (c) 2017-2019 NVIDIA CORPORATION. All rights reserved.
# This file is part of webloader (see TBD).
# See the LICENSE file for licensing terms (BSD-style).
#
from __future__ import unicode_literals

import os
import sys
import subprocess

def run(script, *args, **kw):
    result = subprocess.check_output(["/bin/bash", "-c", script]).decode("utf-8")
    for arg in args:
        assert arg in result, (arg, result)

def test_tar2tsv():
    run("./tar2tsv --help",
        "Extract textual")

def test_tarcats():
    run("./tarcats --help",
        "Concatenate")

def test_tarfirst():
    run("./tarfirst --help",
        "Dump the")

def test_tarmix():
    run("./tarmix --help",
        "specified by a YAML")

def test_tarproc():
    run("./tarproc --help",
        "Each sample is extracted")

def test_tarshow():
    run("./tarshow --help",
        "Show data inside")

def test_tarshow2():
    run("./tarshow testdata/imagenet-000000.tar",
        "b'746'",
        "n07734744")

def test_tarsort():
    run("./tarsort --help",
        "Sort the samples inside")

def test_tarsplit():
    run("./tarsplit --help",
        "Split a tar")

def test_tsv2tar():
    run("./tsv2tar --help",
        "Create a tar file")
