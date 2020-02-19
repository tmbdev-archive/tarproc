#!/usr/bin/python3
#
# Copyright (c) 2017-2019 NVIDIA CORPORATION. All rights reserved.
# This file is part of webloader (see TBD).
# See the LICENSE file for licensing terms (BSD-style).
#

import io
import sys
import tarfile
import time
from urllib.parse import urlparse

__all__ = "TarWriter1 TarWriter".split()


class TarWriter1(object):
    """ """

    def __init__(self, fileobj, keep_meta=False, user="bigdata", group="bigdata", mode=0o0444, compress=None, encoder=None, output_mode=None):
        """A class for writing dictionaries to tar files.

        :param fileobj: fileobj: file name for tar file (.tgz)
        :param bool: keep_meta: keep fields starting with "_"
        :param keep_meta:  (Default value = False)
        :param encoder: sample encoding (Default value = None)
        :param compress:  (Default value = None)
        """
        if isinstance(fileobj, str):
            if compress is False:
                tarmode = "w|"
            elif compress is True:
                tarmode = "w|gz"
            else:
                tarmode = "w|gz" if fileobj.endswith("gz") else "w|"
            if fileobj == "-":
                fileobj = sys.stdout.buffer
            else:
                fileobj = open(fileobj, "wb")
        else:
            tarmode = "w|gz" if compress is True else "w|"
        self.encoder = lambda x: x if encoder is None else encoder
        self.keep_meta = keep_meta
        self.stream = fileobj
        self.tarstream = tarfile.open(fileobj=fileobj, mode=tarmode)

        self.user = user
        self.group = group
        self.mode = mode
        self.compress = compress

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the tar file."""
        self.tarstream.close()
        if self.stream:
            self.stream.close()

    def write(self, obj):
        """Write a dictionary to the tar file.

        :param obj: dictionary of objects to be stored
        :returns: size of the entry

        """
        total = 0
        obj = self.encoder(obj)
        assert "__key__" in obj, "object must contain a __key__"
        for k, v in list(obj.items()):
            if k[0] == "_":
                continue
            assert isinstance(v, bytes), \
                "{} doesn't map to a bytes after encoding ({})".format(k, type(v))
        key = obj["__key__"]
        for k in sorted(obj.keys()):
            if k == "__key__":
                continue
            if not self.keep_meta and k[0] == "_":
                continue
            v = obj[k]
            if isinstance(v, str):
                v = v.encode("utf-8")
            assert isinstance(v, (bytes)),  \
                "converter didn't yield bytes: %s" % ((k, type(v)),)
            now = time.time()
            if isinstance(key, bytes):
                key = key.decode("utf-8")
            fname = str(key + "." + k)
            ti = tarfile.TarInfo(fname)
            ti.size = len(v)
            ti.mtime = now
            ti.mode = self.mode
            ti.uname = self.user
            ti.gname = self.group
            # Since, you are writing to file, it should be of type bytes
            assert isinstance(v, bytes), type(v)
            stream = io.BytesIO(v)
            self.tarstream.addfile(ti, stream)
            total += ti.size
        return total


zmq_schemes = set("zpush zpull zpub zsub zrpush zrpull zrpub zrsub".split())


def TarWriter(url, **kw):
    """Write either to a URL or a ZMQ stream.

    :param url: output URL
    :param **kw: other parameters
    """
    if not isinstance(url, (str, list)):
        return TarWriter1(url, **kw)
    addr = urlparse(url if isinstance(url, str) else url[0])
    scheme, transport = (addr.scheme.split("+", 2) + ["tcp"])[:2]
    if scheme in zmq_schemes:
        from . import zcom
        return zcom.MultiWriter(url, **kw)
    else:
        return TarWriter1(url, **kw)
