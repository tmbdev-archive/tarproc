#
# Copyright (c) 2017-2019 NVIDIA CORPORATION. All rights reserved.
# This file is part of webloader (see TBD).
# See the LICENSE file for licensing terms (BSD-style).
#

import os
import subprocess

from tarproclib import paths


def test_filebase():
    assert paths.filebase("hello/world/a.b.c") == "hello/world/a"


def test_fullext():
    assert paths.fullext("hello/world/a.b.c") == "b.c"
