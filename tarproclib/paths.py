#!/usr/bin/python3
#
# Copyright (c) 2017-2019 NVIDIA CORPORATION. All rights reserved.
# This file is part of webloader (see TBD).
# See the LICENSE file for licensing terms (BSD-style).
#

import os
import re


def filebase(fname):
    return re.sub(r"\.[^/]*$", "", fname)


def fullext(fname):
    return re.sub(r"(.*/)*.*?\.", "", fname)


def read_binary(fname):
    with open(fname, "rb") as stream:
        return stream.read()


def write_binary(fname, data):
    with open(fname, "wb") as stream:
        if isinstance(data, str):
            data = data.encode("utf-8")
        stream.write(data)


class ChDir(object):
    def __init__(self, path):
        self.old_dir = os.getcwd()
        self.new_dir = path

    def __enter__(self):
        os.chdir(self.new_dir)

    def __exit__(self, *args):
        os.chdir(self.old_dir)


class FilePlusExt:
    def __init__(self, path):
        self.path = path

    def base(self):
        return re.sub(r"\.[^/]*$", "", self.path)

    def key(self):
        return re.sub(r"(.*/)*.*?\.", "", self.path)


class DirPlusFile:
    def __init__(self, path):
        self.path = path

    def base(self):
        return re.sub(r".*/", "", self.path)

    def key(self):
        return re.sub(r"[^/]*$", "", self.path)


def base_plus_ext(path):
    """Helper method that splits off all extension.

    Returns base, allext.

    :param path: path with extensions
    :returns: path with all extensions removed

    """
    match = re.match(r"^((?:.*/|)[^.]+)[.]([^/]*)$", path)
    if not match:
        return None, None
    return match.group(1), match.group(2)


def dir_plus_file(path):
    """Helper method that splits off all extension.

    Returns base, allext.

    :param path: path with extensions
    :returns: path with all extensions removed

    """
    match = re.match(r"^(.*)/([^/]*)$", path)
    if not match:
        return None, None
    return match.group(1), match.group(2)
