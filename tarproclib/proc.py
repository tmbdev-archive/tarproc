#!/usr/bin/python3
#
# Copyright (c) 2017-2019 NVIDIA CORPORATION. All rights reserved.
# This file is part of webloader (see TBD).
# See the LICENSE file for licensing terms (BSD-style).
#

import random


def ishuffle(data, bufsize=1000, initial=100):
    """Shuffle the data in the stream.

    This uses a buffer of size `bufsize`. Shuffling at
    startup is less random; this is traded off against
    yielding samples quickly.

    :param data: iterator
    :param bufsize: buffer size for shuffling
    :returns: iterator

    """
    if bufsize < 2:
        for sample in data:
            yield sample
        return
    initial = min(initial, bufsize)
    buf = []
    startup = True
    for sample in data:
        if len(buf) < bufsize:
            buf.append(next(data))
        k = random.randint(0, len(buf) - 1)
        sample, buf[k] = buf[k], sample
        if startup and len(buf) < initial:
            buf.append(sample)
            continue
        startup = False
        yield sample
    for sample in buf:
        yield sample
