#!/usr/bin/python3
#
# Copyright (c) 2017-2019 NVIDIA CORPORATION. All rights reserved.
# This file is part of webloader (see TBD).
# See the LICENSE file for licensing terms (BSD-style).
#

import os
import re
import subprocess
import sys
import time

bufsize = 8192


class GopenException(Exception):
    def __init__(self, info):
        super().__init__()
        self.info = info


class Pipe(object):
    def __init__(self, *args, raise_errors=True, **kw):
        self.open(*args, **kw)
        self.raise_errors = raise_errors

    def open(self, *args, **kw):
        self.proc = subprocess.Popen(*args, bufsize=bufsize, stdout=subprocess.PIPE, **kw)
        self.args = (args, kw)
        self.stream = self.proc.stdout
        if self.stream is None:
            raise GopenException(f"{self.args}: no stream (open)")
        self.status = None
        return self

    def read(self, *args, **kw):
        result = self.stream.read(*args, **kw)
        self.status = self.proc.poll()
        if self.status is not None:
            self.status = self.proc.wait()
            if self.status != 0 and self.raise_errors:
                raise GopenException(f"{self.args}: exit {self.status} (read)")
        return result

    def readLine(self, *args, **kw):
        result = self.stream.readLine(*args, **kw)
        self.status = self.proc.poll()
        if self.status is not None:
            self.status = self.proc.wait()
            if self.status != 0 and self.raise_errors:
                raise GopenException(f"{self.args}: exit {self.status} (readLine)")
        return result

    def close(self):
        self.stream.close()
        try:
            self.status = self.proc.wait(1.0)
        except subprocess.TimeoutExpired:
            self.proc.terminate()
            time.sleep(0.1)
            self.proc.kill()
            self.status = self.proc.wait(1.0)
        if self.raise_errors == "all":
            if self.status != 0 and self.raise_errors:
                raise GopenException(f"{self.args}: exit {self.status} (close)")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()


prefix = "GOPEN_"

handlers = {
    "gs": "gsutil cat '{}'",
    "http": "curl --fail -L -s '{}' --output -",
    "https": "curl --fail -L -s '{}' --output -",
    "file": "dd if='{}' bs=4M"
}

handlers.update({
    k[len(prefix):].lower(): v
    for k, v in os.environ.items()
    if k.startswith(prefix)
})


def gopen(url, mode="rb"):
    """Open a stream using different handlers.

    :param url: url to be opened
    :param mode: read or write
    """
    if url == "-":
        if "w" in mode:
            stream = sys.stdout
        else:
            stream = sys.stdin
        if "b" in mode:
            stream = stream.buffer
        return stream
    if url.lower().startswith("file:"):
        url = url[5:]
        return open(url, mode)
    match = re.search(r"^([a-z]+):(?i)", url)
    if not match:
        return open(url, mode)
    schema = match.group(1).lower()
    handler = handlers.get(schema)
    if handler is None:
        raise ValueError(f"{url}: no {prefix}{schema} handler in environment")
    cmd = handler.format(url)
    if int(os.environ.get("GOPEN_DEBUG", "0")):
        print("#", cmd, file=sys.stderr)
    return Pipe(cmd, shell=True)
