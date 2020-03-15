#!/usr/bin/python3
#
# Copyright (c) 2017-2019 NVIDIA CORPORATION. All rights reserved.
# This file is part of webloader (see TBD).
# See the LICENSE file for licensing terms (BSD-style).
#

import io
import subprocess
import sys

bufsize = 8192

processes = []


def maybe_wait(proc):
    status = proc.poll()
    if status is not None:
        status = proc.wait()
        if status != 0:
            return status
        return False
    return True


def collect_processes():
    global processes
    results = [(proc, maybe_wait(proc)) for proc in processes]
    processes = [proc for proc, status in results if status is True]
    for proc, status in results:
        if status not in [False, True]:
            raise subprocess.CalledProcessError(status, proc.gopen_command)


def open_std(mode):
    if "w" in mode:
        stream = sys.stdout
    else:
        stream = sys.stdin
    if "b" in mode:
        stream = stream.buffer
    return stream


def open_pipe(cmd, mode):
    kw = dict(stderr=sys.stderr)
    if mode[0] == "r":
        kw["stdout"] = subprocess.PIPE
    else:
        kw["stdin"] = subprocess.PIPE
    proc = subprocess.Popen(cmd, shell=True, **kw)
    proc.gopen_command = cmd
    stream = proc.stdout if mode[0] == "r" else proc.stdin
    if "b" not in mode:
        stream = io.TextIOWrapper(stream)
    return stream


def gopen(url, mode="rb", collect=True):
    """Open an I/O stream. This understands:

    "-": stdin/stdout
    "pipe:cmd": opens a pipe to the given command
    anything else: opens as a file

    If you use "pipe:", this will attempt to harvest previous processes
    and may give an exception unrelated to the current `gopen`. Call `collect_processes`
    explicitly to avoid this.

    :param url: url to be opened
    :param mode: one of "r", "w", "rb", or "wb"
    """

    assert mode in ["r", "w", "rb", "wb"]

    if url == "-":
        return open_std(mode)

    if url.startswith("pipe:"):
        if collect:
            collect_processes()
        return open_pipe(url[5:], mode)

    return open(url, mode)
