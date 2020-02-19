#!/usr/bin/python3
#
# Copyright (c) 2017-2019 NVIDIA CORPORATION. All rights reserved.
# This file is part of webloader (see TBD).
# See the LICENSE file for licensing terms (BSD-style).
#

__all__ = "tariterator TarIterator1 TarIterator".split()

import math
import random
import re
import sys
import tarfile
from urllib.parse import urlparse

import braceexpand as braceexpandlib

from . import gopen, paths

meta_prefix = "__"
meta_suffix = "__"


def regquote(s):
    """Quote regular expressions.

    :param s: string to be quoted.
    """
    return re.sub(r'([][.^$*+])', r'\\\1', s)


def valid_sample(sample):
    """Check whether the sample is valid (not empty and not None).

    :param sample: sample, should be a dict
    """
    return sample is not None and sample != {}


def tardata(fileobj, skip_meta=r"__[^/]*__($|/)"):
    """Iterator yielding filename, content pairs for the given tar stream.

    :param fileobj: byte stream suitable for tarfile
    :param skip_meta: regexp for keys that are skipped entirely (Default value = r"__[^/]*__($|/)")

    """
    stream = tarfile.open(fileobj=fileobj, mode="r|*")
    for tarinfo in stream:
        if not tarinfo.isreg():
            continue
        fname = tarinfo.name
        if fname is None:
            continue
        if "/" not in fname and fname.startswith(meta_prefix) and fname.endswith(meta_suffix):
            # skipping metadata for now
            continue
        if skip_meta is not None and re.match(skip_meta, fname):
            continue
        data = stream.extractfile(tarinfo).read()
        yield fname, data
    del stream


def group_by_keys(keys=paths.base_plus_ext, lcase=True, suffixes=None):
    """Returns function over iterator that groups key, value pairs into samples.

    :param keys: function that splits the key into key and extension (Default value = base_plus_ext)
    :param lcase: convert suffixes to lower case (Default value = True)

    """
    def iterator(data):
        current_sample = None
        for fname, value in data:
            prefix, suffix = keys(fname)
            if prefix is None:
                continue
            if current_sample is not None and prefix == current_sample["__key__"]:
                current_sample[suffix] = value
                continue
            if valid_sample(current_sample):
                yield current_sample
            current_sample = dict(__key__=prefix)
            if lcase:
                suffix = suffix.lower()
            if suffixes is None or suffix in suffixes:
                current_sample[suffix] = value
        if valid_sample(current_sample):
            yield current_sample
    return iterator


def tariterator(fileobj, keys=paths.base_plus_ext, decoder=None, suffixes=None, errors=True, container=None):
    """Iterate through training samples stored in a sharded tar file.

    :param fileobj:
    :param check_sorted:  (Default value = False)
    :param keys:  (Default value = base_plus_ext)
    :param decode:  (Default value = True)

    """
    content = tardata(fileobj)
    samples = group_by_keys(keys=keys, suffixes=suffixes)(content)
    if decoder is not None:
        samples = (decoder(sample) for sample in samples)
    return samples


class TarIterator1(object):
    """Iterate of tar files consisting of samples.

    :param url: source URL
    :param braceexpand: expand braces in the source URL
    :param shuffle: shuffle the samples
    :param allow_missing: allow missing shards
    :param **kw:
    """
    def __init__(self, url, braceexpand=True, shuffle=False, allow_missing=False, **kw):
        self.start = 0
        self.end = math.inf
        self.allow_missing = allow_missing
        if len(url.rsplit("#", 1)) > 1:
            url, fragment = url.rsplit("#", 1)
            self.start, self.end = [int(x) for x in (fragment.rsplit(",") * 2)[:2]]
            self.end += 1
        if braceexpand:
            self.urls = list(braceexpandlib.braceexpand(url))
        else:
            self.urls = [url]
        if shuffle:
            random.shuffle(self.urls)
        self.kw = kw

    def __iter__(self):
        count = 0
        for url in self.urls:
            try:
                with gopen.gopen(url, "rb") as stream:
                    for sample in tariterator(stream, **self.kw):
                        if count < self.start:
                            continue
                        if count >= self.end:
                            break
                        if "__source__" not in sample:
                            sample["__source__"] = url
                        yield sample
                        count += 1
            except gopen.GopenException as e:
                if self.allow_missing:
                    print(e.info, file=sys.stderr)
                else:
                    raise e
            if count >= self.end:
                break


zmq_schemes = set("zpush zpull zpub zsub zrpush zrpull zrpub zrsub".split())


def TarIterator(url, **kw):
    """Open an iterator of tar files.

    This can open either ZMQ URLs or object store URLs.

    :param url: source URL
    :param **kw:
    """
    if not isinstance(url, (str, list)):
        return TarIterator1(url, **kw)
    addr = urlparse(url if isinstance(url, str) else url[0])
    scheme, transport = (addr.scheme.split("+", 2) + ["tcp"])[:2]
    if scheme in zmq_schemes:
        from . import zcom
        return zcom.Connection(url, **kw)
    else:
        return TarIterator1(url, **kw)
